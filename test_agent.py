import requests
import time

url = "http://localhost:8000/api/agent/execute"

def testar_agente():
    print("🧪 Testando Agente ORVION...\n")
    comandos = [
        "Envia 10 USDC pra minha wallet",
        "Cria um job de escrow de 50 USDC",
        "Pesquisa agentes para swap de ETH",
        "Qual é meu saldo atual?"
    ]
    
    for cmd in comandos:
        print(f"👤 Você: {cmd}")
        try:
            resp = requests.post(url, json={
                "command": cmd,
                "wallet_address": "0x41975126c6465e2d42bd75154867d75604fd67a2da40a91d2ab3489cac9186c8"
            }, timeout=30)
            print("🤖 Agente:", resp.json().get("response", "Sem resposta")[:300] + "...\n")
        except Exception as e:
            print(f"❌ Erro ao testar comando '{cmd}': {e}\n")
        time.sleep(2)

if __name__ == "__main__":
    testar_agente()
