<p align="center">
  <img src="public/brand/logo.png" width="200" alt="Pocket Oracle Logo">
</p>

<h1 align="center">Pocket Oracle</h1>

<p align="center">
  <strong>The Phone as an Agent Marketplace</strong><br>
  <em>Transformando smartphones em oráculos monetizáveis do mundo real para agentes de IA.</em>
</p>

<p align="center">
  <a href="#-visão-executiva">Visão Executiva</a> •
  <a href="#-arquitetura">Arquitetura</a> •
  <a href="#-funcionalidades-atuais">Funcionalidades</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-segurança">Segurança</a> •
  <a href="README.en.md">English Version</a>
</p>

<img src="public/brand/banner.png" width="100%" alt="Pocket Oracle Banner">

---

## 👁️ Visão Executiva

O **Pocket Oracle** resolve o gargalo de confiança entre o mundo digital e o físico. Quando um agente de IA precisa de uma confirmação do mundo real, ele não deve depender de processos manuais lentos. Ele deve ser capaz de **pagar centavos, receber uma resposta verificável e continuar sua execução em tempo real**.

Nossa tese é transformar cada smartphone em um nó de uma rede de oráculos descentralizada, onde a verificação humana e os sinais contextuais são ativos monetizáveis.

---

## 🏗️ Arquitetura

O projeto é estruturado como um monorepo de nível industrial, garantindo escalabilidade e separação clara de responsabilidades.

<img src="public/brand/architecture.png" width="100%" alt="Pocket Oracle Architecture">

| Camada | Papel Estratégico |
| :--- | :--- |
| **Gateway Pago** | Implementa o fluxo comercial e o comportamento `402 Payment Required`. |
| **Operação Mobile** | PWA que transforma o smartphone no centro da coleta de dados. |
| **Sensor Orchestrator** | Inteligência em FastAPI para OCR, Geoproof e validação humana. |
| **Admin Dashboard** | Visão executiva de métricas, estado da demo e governança. |
| **Infraestrutura** | Ambiente Dockerizado para evolução previsível e segura. |

---

## 🚀 Funcionalidades Atuais

A versão atual entrega o esqueleto funcional para uma demonstração de alto impacto com narrativa econômica forte.

| Serviço | Descrição | Preço Sugerido |
| :--- | :--- | :--- |
| **GeoProof** | Evidência contextual de localização verificável. | `0.0015` |
| **SnapOCR** | Extração de texto de ambientes físicos via câmera. | `0.0040` |
| **HumanTap** | Confirmação humana rápida, auditável e segura. | `0.0060` |

---

## 🗺️ Roadmap Estratégico

Estamos construindo mais do que um protótipo; estamos definindo um novo mercado de microserviços físicos para agentes.

<img src="public/brand/roadmap_visual.png" width="100%" alt="Pocket Oracle Roadmap">

### Fase 1: Demo Funcional (Atual)
- [x] PWA Mobile operacional.
- [x] Gateway com suporte a `402 Payment Required`.
- [x] Orquestrador de sensores básico.

### Fase 2: Liquidação Real
- [ ] Integração com wallets e micropagamentos.
- [ ] Provas auditáveis on-chain.
- [ ] Sistema de reputação inicial.

### Fase 3: Submission Grade
- [ ] Deploy em larga escala.
- [ ] Documentação técnica ultra-profunda.
- [ ] Vídeo de pitch e materiais de marketing.

### Fase 4: Produto Real
- [ ] Marketplace multi-device.
- [ ] SLAs garantidos por staking.
- [ ] Roteamento inteligente de tarefas.

---

## 🛡️ Segurança e Governança

Como um projeto de nível CEO, a segurança não é opcional. Seguimos as melhores práticas de higiene operacional:

- **Higiene de Segredos:** Nunca fazemos commit de arquivos `.env` ou credenciais.
- **Branch Protection:** A branch `main` é protegida e requer revisão.
- **Scanning:** Monitoramento contínuo de vulnerabilidades em dependências.

---

## 🛠️ Quick Start

```bash
# Clonar e configurar
git clone https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace.git
cd Pocket-Oracle-The-Phone-as-an-Agent-Marketplace

# Subir infraestrutura
docker compose -f infra/docker/docker-compose.yml up -d

# Iniciar serviços
npm install
npm run dev:api
```

---

<p align="center">
  Desenvolvido com foco em excelência técnica e visão de mercado.<br>
  <strong>Pocket Oracle © 2026</strong>
</p>
