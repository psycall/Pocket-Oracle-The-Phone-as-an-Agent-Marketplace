
# Copyright © 2026 ORVION. All rights reserved.
# Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

import json
import logging
import os
from typing import List, Optional
from uuid import uuid4

from sqlalchemy.orm import Session
from web3 import Web3
from web3.exceptions import ContractLogicError

from . import models, schemas, notifications, graph_engine
from .config import settings

logger = logging.getLogger(__name__)

# ─── Web3 & Contract Initialisation ─────────────────────────────────────────

w3 = Web3(Web3.HTTPProvider(settings.ARC_RPC_URL))

# ABI mínimo necessário para o contrato Orvion
_ORVION_ABI = [
    {
        "inputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}],
        "name": "settleJob",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}],
        "name": "completeJob",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_worker", "type": "address"},
            {"internalType": "uint256", "name": "_amount", "type": "uint256"},
            {"internalType": "bytes32", "name": "_jobHash", "type": "bytes32"},
        ],
        "name": "createJob",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "jobCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "jobs",
        "outputs": [
            {"internalType": "address", "name": "creator", "type": "address"},
            {"internalType": "address", "name": "worker", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint8", "name": "status", "type": "uint8"},
            {"internalType": "bytes32", "name": "jobHash", "type": "bytes32"},
            {"internalType": "uint256", "name": "createdAt", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]

# ABI mínimo para o token USDC (ERC20)
_USDC_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"name": "remaining", "type": "uint256"}],
        "type": "function",
    },
]

orvion_contract = w3.eth.contract(
    address=Web3.to_checksum_address(settings.SETTLEMENT_CONTRACT_ADDRESS),
    abi=_ORVION_ABI,
)

usdc_contract = w3.eth.contract(
    address=Web3.to_checksum_address(settings.USDC_CONTRACT),
    abi=_USDC_ABI,
)

# Suporte ao novo token cirBTC na Arc Testnet
cirbtc_contract = w3.eth.contract(
    address=Web3.to_checksum_address(settings.CIRBTC_CONTRACT),
    abi=_USDC_ABI, # cirBTC segue o padrão ERC20
)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def _has_signer() -> bool:
    """Retorna True se uma chave privada válida estiver configurada."""
    return bool(settings.PRIVATE_KEY and settings.PRIVATE_KEY.startswith("0x") and len(settings.PRIVATE_KEY) == 66)


def _send_transaction(fn_call) -> str:
    """
    Assina e envia uma transação ao contrato Orvion.
    Retorna o hash da transação em hex.
    Lança RuntimeError se a chave privada não estiver configurada.
    """
    if not _has_signer():
        raise RuntimeError(
            "PRIVATE_KEY não configurada. Defina PRIVATE_KEY no .env para enviar transações reais."
        )

    account = w3.eth.account.from_key(settings.PRIVATE_KEY)
    nonce = w3.eth.get_transaction_count(account.address)
    chain_id = settings.ARC_CHAIN_ID

    tx = fn_call.build_transaction({
        "from": account.address,
        "nonce": nonce,
        "chainId": chain_id,
        "gas": 200_000,
        "gasPrice": w3.eth.gas_price,
    })

    signed = w3.eth.account.sign_transaction(tx, settings.PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

    if receipt.status != 1:
        # Categorização de erro inspirada no Bridge Kit 1.9.0
        error_msg = f"Transação revertida on-chain: {tx_hash.hex()}"
        logger.error(f"[ONCHAIN_FAILURE] {error_msg}")
        raise RuntimeError(error_msg)

    return tx_hash.hex()


def _get_usdc_contract_for_network(chain_id: int = None):
    """Retorna o contrato USDC correto baseado no Chain ID."""
    if chain_id is None or chain_id == settings.ARC_CHAIN_ID:
        return usdc_contract
    
    # Busca no registry multichain
    for domain, info in settings.MULTICHAIN_REGISTRY.items():
        if info["chain_id"] == chain_id:
            return w3.eth.contract(
                address=Web3.to_checksum_address(info["usdc"]),
                abi=_USDC_ABI
            )
    return usdc_contract

def _ensure_usdc_approval(amount_wei: int, chain_id: int = None):
    """Garante que o contrato Orvion tenha permissão para gastar USDC na rede especificada."""
    if not _has_signer():
        return

    account = w3.eth.account.from_key(settings.PRIVATE_KEY)
    spender = Web3.to_checksum_address(settings.SETTLEMENT_CONTRACT_ADDRESS)
    
    target_usdc = _get_usdc_contract_for_network(chain_id)
    allowance = target_usdc.functions.allowance(account.address, spender).call()
    
    if allowance < amount_wei:
        logger.info(f"Aprovando USDC na rede {chain_id or 'Arc'} para o contrato Orvion...")
        fn_call = target_usdc.functions.approve(spender, 2**256 - 1)
        _send_transaction(fn_call)


# ─── CRUD ─────────────────────────────────────────────────────────────────────

def create_settlement(db: Session, settlement: schemas.SettlementCreate):
    on_chain_id = getattr(settlement, "on_chain_job_id", None)
    
    # ─── MVP PHASE 1: AUTOMATED ON-CHAIN ESCROW ──────────────────────────────
    if on_chain_id is None and _has_signer() and w3.is_connected():
        try:
            # USDC typically has 6 decimals, but we check for flexibility
            amount_wei = int(settlement.amount * 10**6)
            _ensure_usdc_approval(amount_wei)
            
            # Create a unique job hash for on-chain verification
            job_hash = w3.keccak(text=f"{settlement.job_id}-{uuid4().hex}")
            
            logger.info(f"Initiating on-chain escrow for Job {settlement.job_id}...")
            fn_call = orvion_contract.functions.createJob(
                Web3.to_checksum_address(settlement.to_address),
                amount_wei,
                job_hash
            )
            tx_hash = _send_transaction(fn_call)
            
            # Fetch the actual job ID from the contract
            on_chain_id = orvion_contract.functions.jobCount().call() - 1
            logger.info(f"✅ On-chain Job Created: ID {on_chain_id} | TX: {tx_hash}")
        except Exception as exc:
            logger.error(f"❌ On-chain escrow failed: {exc}. Falling back to local tracking.")

    db_settlement = models.Settlement(
        id=str(uuid4()),
        agent_id=settlement.agent_id,
        job_id=settlement.job_id,
        amount=settlement.amount,
        to_address=settlement.to_address,
        status="pending",
        on_chain_job_id=on_chain_id,
    )
    db.add(db_settlement)
    db.commit()
    db.refresh(db_settlement)

    # Notificação em tempo real via WebSocket
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(notifications.manager.send_personal_message(
                {"type": "settlement_created", "data": schemas.Settlement.model_validate(db_settlement).model_dump()},
                db_settlement.user_id if hasattr(db_settlement, "user_id") else "system",
            ))
    except Exception:
        pass

    return db_settlement


def get_settlement(db: Session, settlement_id: str):
    return db.query(models.Settlement).filter(models.Settlement.id == settlement_id).first()


def get_agent_settlements(db: Session, agent_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Settlement).filter(models.Settlement.agent_id == agent_id).offset(skip).limit(limit).all()

def create_execution_receipt(db: Session, receipt: schemas.ExecutionReceiptCreate):
    """
    Submete um recibo de execução para um job.
    Isso dispara a verificação e prepara o job para liquidação.
    """
    db_receipt = models.ExecutionReceipt(
        id=str(uuid4()),
        job_id=receipt.job_id,
        proof=receipt.proof,
        verified=True # MVP: Auto-verificação para o fluxo atômico
    )
    db.add(db_receipt)
    
    # Atualiza o status do job para 'completed'
    job = db.query(models.Job).filter(models.Job.id == receipt.job_id).first()
    if job:
        job.status = "completed"
        db.add(job)
        
    db.commit()
    db.refresh(db_receipt)
    return db_receipt

def get_execution_receipt(db: Session, receipt_id: str):
    return db.query(models.ExecutionReceipt).filter(models.ExecutionReceipt.id == receipt_id).first()

def process_settlement_batch(db: Session, settlements: List[models.Settlement]) -> str:
    """
    Processa um lote de liquidações pendentes.

    Comportamento:
    - Se PRIVATE_KEY estiver configurada e a rede Arc estiver acessível, chama
      `settleJob(on_chain_job_id)` no contrato Orvion para cada liquidação que
      possua um `on_chain_job_id` válido.
    - Se a chave não estiver configurada ou a rede estiver indisponível, registra
      o aviso e confirma localmente (modo fallback), preservando a operação do
      sistema sem interromper o fluxo.

    Retorna o hash da última transação enviada (ou um hash local no fallback).
    """
    last_tx_hash: Optional[str] = None
    connected = w3.is_connected()

    if not connected:
        logger.warning(
            "Arc Testnet inacessível via %s — processando em modo fallback local.",
            settings.ARC_RPC_URL,
        )

    for settlement in settlements:
        on_chain_id: Optional[int] = getattr(settlement, "on_chain_job_id", None)
        tx_hash: Optional[str] = None

        # Tenta liquidação real on-chain
        if connected and _has_signer() and on_chain_id is not None:
            try:
                fn_call = orvion_contract.functions.settleJob(int(on_chain_id))
                tx_hash = _send_transaction(fn_call)
                logger.info(
                    "settleJob(%s) confirmado on-chain — tx: %s", on_chain_id, tx_hash
                )
            except ContractLogicError as exc:
                logger.error(
                    "Contrato reverteu settleJob(%s): %s — marcando como failed.", on_chain_id, exc
                )
                settlement.status = "failed"
                settlement.transaction_hash = None
                db.add(settlement)
                continue
            except Exception as exc:
                logger.error(
                    "Erro ao enviar settleJob(%s): %s — usando fallback.", on_chain_id, exc
                )
                tx_hash = None

        # Fallback: confirma localmente quando on-chain não é possível
        if tx_hash is None:
            reason = (
                "on_chain_job_id ausente" if on_chain_id is None
                else "PRIVATE_KEY não configurada" if not _has_signer()
                else "rede indisponível"
            )
            logger.warning(
                "Settlement %s confirmado localmente (%s).", settlement.id, reason
            )
            tx_hash = "0x" + uuid4().hex

        settlement.status = "confirmed"
        settlement.transaction_hash = tx_hash
        last_tx_hash = tx_hash
        db.add(settlement)

        # Atualiza Reputation Graph (Neo4j)
        try:
            graph_engine.graph_engine.update_agent_reputation(
                agent_address=settlement.to_address,
                job_id=settlement.job_id,
                amount=float(settlement.amount),
                status="confirmed",
            )
        except Exception as exc:
            logger.warning("Falha ao atualizar reputation graph: %s", exc)

        # Notificação em tempo real via WebSocket
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(notifications.manager.send_personal_message(
                    {
                        "type": "settlement_confirmed",
                        "settlement_id": settlement.id,
                        "tx_hash": tx_hash,
                        "on_chain": tx_hash and not tx_hash.startswith("0x") or len(tx_hash) == 66,
                    },
                    settlement.user_id if hasattr(settlement, "user_id") else "system",
                ))
        except Exception:
            pass

    db.commit()
    return last_tx_hash or ("0x" + uuid4().hex)


# ─── Execution Receipts ───────────────────────────────────────────────────────

def create_execution_receipt(db: Session, receipt: schemas.ExecutionReceiptCreate):
    # Tenta marcar o job como completo on-chain se houver um settlement associado
    settlement = db.query(models.Settlement).filter(models.Settlement.job_id == receipt.job_id).first()
    on_chain_success = False
    
    if settlement and settlement.on_chain_job_id is not None and _has_signer() and w3.is_connected():
        try:
            fn_call = orvion_contract.functions.completeJob(int(settlement.on_chain_job_id))
            tx_hash = _send_transaction(fn_call)
            logger.info("Job %s marcado como completo on-chain: %s", settlement.on_chain_job_id, tx_hash)
            on_chain_success = True
        except Exception as exc:
            logger.error("Falha ao completar job on-chain: %s", exc)

    db_receipt = models.ExecutionReceipt(
        id=str(uuid4()),
        job_id=receipt.job_id,
        proof=receipt.proof,
        verified=on_chain_success, # Marcado como verificado se a transação on-chain teve sucesso
    )
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt


def get_execution_receipt(db: Session, receipt_id: str):
    return db.query(models.ExecutionReceipt).filter(models.ExecutionReceipt.id == receipt_id).first()
