# Orvion Setup Guide

**PT-BR** | **EN**

Este guia concentra o passo a passo operacional do **Orvion** para quem precisa sair de um repositório recém-clonado até uma execução local organizada, segura e pronta para demonstração. O objetivo é reduzir ambiguidade, acelerar onboarding e garantir que a experiência pública do projeto continue coerente com um padrão de startup premium.

| Seção | Finalidade |
| --- | --- |
| Preparação | Validar ambiente, credenciais e postura de segurança |
| Instalação | Subir dependências Node.js, Python e infraestrutura local |
| Execução | Rodar gateway, PWA, dashboard e orquestrador |
| Validação | Confirmar health checks, pricing e fluxo `402 -> retry` |
| Publicação | Aplicar governança no GitHub e preparar o perfil público |

## PT-BR

### 1. Visão geral do fluxo

A ordem recomendada é simples: primeiro você prepara o ambiente local e revisa segredos; depois sobe infraestrutura, backend e interfaces; em seguida valida os endpoints centrais; por fim, aplica os controles de governança do GitHub e a apresentação pública do projeto. Essa sequência reduz retrabalho e preserva segurança operacional desde o início.

| Etapa | Resultado esperado |
| --- | --- |
| Preparação do ambiente | Node, Python, Docker e Git funcionando |
| Configuração local | `.env.local` criado sem expor segredos |
| Infraestrutura | Postgres e Redis ativos via Docker Compose |
| Serviços | API Gateway, PWA, Dashboard e FastAPI respondendo |
| Governança | Branch protection, revisão obrigatória e scanning habilitados |

### 2. Pré-requisitos

O monorepo foi estruturado para ambiente moderno de desenvolvimento. A base usa **Node.js 22+**, **Python 3.11+** e **Docker Compose** para orquestrar a infraestrutura local. O GitHub recomenda proteger a branch principal, exigir revisão em mudanças sensíveis e ativar mecanismos de segurança do repositório para reduzir risco operacional [1] [2].

| Dependência | Versão recomendada | Observação |
| --- | --- | --- |
| Node.js | `22.x` ou superior | Necessário para workspaces e builds locais |
| npm | Compatível com Node 22 | Instalado junto com Node |
| Python | `3.11` ou superior | Necessário para o serviço FastAPI |
| Docker | Atual | Recomendado com Compose habilitado |
| Git | Atual | Necessário para fluxo de colaboração e publicação |

### 3. Clonagem e preparação inicial

Se o repositório ainda não estiver localmente disponível, clone-o e entre na pasta principal. Em seguida, crie o arquivo local de ambiente a partir do exemplo e revise cada variável antes de rodar qualquer serviço.

```bash
git clone https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace.git
cd Pocket-Oracle-The-Phone-as-an-Agent-Marketplace
cp .env.example .env.local
```

> Nunca versione `.env.local`, chaves privadas, tokens ou credenciais temporárias. Qualquer segredo exposto deve ser tratado como comprometido imediatamente.

### 4. Instalação das dependências do monorepo

Instale primeiro as dependências JavaScript do workspace raiz. Depois prepare um ambiente virtual Python dedicado para o orquestrador de sensores.

```bash
npm install
python3 -m venv .venv
source .venv/bin/activate
pip install -r services/sensor-orchestrator/requirements.txt
```

### 5. Subida da infraestrutura local

O projeto utiliza Docker Compose para inicializar os serviços de suporte ao fluxo de demonstração e evolução do MVP.

```bash
docker compose -f infra/docker/docker-compose.yml up -d
```

Depois, confirme se os containers estão ativos:

```bash
docker compose -f infra/docker/docker-compose.yml ps
```

### 6. Execução dos serviços principais

Abra terminais separados para manter visibilidade operacional. A divisão abaixo ajuda a detectar falhas rapidamente.

| Terminal | Comando | Papel |
| --- | --- | --- |
| 1 | `npm run dev:api` | Sobe o gateway de pagamentos e endpoints pagos |
| 2 | `npm run dev:mobile` | Sobe a experiência mobile-first |
| 3 | `npm run dev:admin` | Sobe o dashboard executivo e operacional |
| 4 | `source .venv/bin/activate && uvicorn app.main:app --app-dir services/sensor-orchestrator --host 0.0.0.0 --port 8100 --reload` | Sobe o serviço FastAPI |

### 7. Validação do fluxo principal

Com a stack rodando, valide primeiro os endpoints de saúde e precificação. Depois teste o comportamento econômico central do produto: uma chamada inicial sem autorização deve retornar **HTTP 402**, e a segunda chamada, com autorização apropriada, deve concluir o fluxo com sucesso.

| Verificação | O que observar |
| --- | --- |
| `GET /health` | Serviço responde sem erro |
| `GET /pricing` | Tabela de preços é retornada corretamente |
| `POST /oracle/geoproof` | Sem autorização, retorno `402` |
| Retry autorizado | Resultado retornado e demo econômica preservada |

### 8. Padrão de segurança para operação e publicação

Antes de qualquer push público, revise postura de segurança. O GitHub documenta branch protection, revisões obrigatórias, status checks e práticas de proteção da cadeia de build como controles essenciais para repositórios públicos e times em crescimento [1] [2].

| Controle | Estado recomendado |
| --- | --- |
| `main` protegida | Ativado |
| Pull request review obrigatório | Ativado |
| Status checks obrigatórios | Ativado |
| Secret scanning | Ativado |
| Dependabot alerts | Ativado |
| Auto-delete de branches após merge | Ativado |

### 9. Publicação do perfil profissional do fundador

O perfil público do GitHub pode exibir um README especial quando existe um repositório público com o mesmo nome do usuário. Para a conta `psycall`, isso significa manter um repositório chamado `psycall` com um `README.md` principal [3]. O material base preparado para isso está em `profile/`.

| Arquivo | Uso |
| --- | --- |
| `profile/README.md` | Conteúdo principal do perfil bilíngue |
| `profile/PROFILE_SETUP.md` | Guia de publicação do perfil |
| `profile/assets/` | Banner e ativos visuais |

### 10. Checklist executivo de pronta execução

Antes de apresentar o projeto para parceiros, jurados ou investidores, confirme se o repositório está não apenas funcional, mas também publicamente convincente.

| Item | Critério de pronto |
| --- | --- |
| README principal | Bilíngue, coerente e com identidade visual premium |
| Segurança | Políticas, scanning e governança ativos |
| Branding | Banner, preview social e logo versionados |
| Demo | Fluxo `402 -> retry` validado |
| Perfil GitHub | README profissional alinhado ao projeto |

## EN

### 1. Flow overview

The recommended order is straightforward: prepare the local environment and review secrets first, then boot infrastructure, backend, and interfaces, validate the key endpoints, and finally apply GitHub governance plus public-facing repository polish. That order reduces rework while preserving a strong operational posture.

### 2. Prerequisites

The monorepo targets a modern developer setup with **Node.js 22+**, **Python 3.11+**, and **Docker Compose**. GitHub recommends protecting the default branch, requiring review for sensitive changes, and enabling repository security controls to reduce operational risk [1] [2].

| Dependency | Recommended version | Notes |
| --- | --- | --- |
| Node.js | `22.x` or later | Required for workspaces and local builds |
| npm | Version aligned with Node 22 | Installed with Node |
| Python | `3.11` or later | Required for the FastAPI service |
| Docker | Current | Prefer Docker with Compose enabled |
| Git | Current | Required for collaboration and publishing |

### 3. Clone and initialize

Clone the repository, enter the project folder, and create the local environment file from the example. Review every variable before starting any service.

```bash
git clone https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace.git
cd Pocket-Oracle-The-Phone-as-an-Agent-Marketplace
cp .env.example .env.local
```

### 4. Install dependencies

Install the JavaScript workspace dependencies first, then prepare a dedicated Python virtual environment for the sensor orchestrator.

```bash
npm install
python3 -m venv .venv
source .venv/bin/activate
pip install -r services/sensor-orchestrator/requirements.txt
```

### 5. Start local infrastructure

```bash
docker compose -f infra/docker/docker-compose.yml up -d
```

Then verify container state:

```bash
docker compose -f infra/docker/docker-compose.yml ps
```

### 6. Run the main services

Use separate terminals for better observability.

| Terminal | Command | Role |
| --- | --- | --- |
| 1 | `npm run dev:api` | Starts the payment gateway and paid endpoints |
| 2 | `npm run dev:mobile` | Starts the mobile-first interface |
| 3 | `npm run dev:admin` | Starts the executive and operational dashboard |
| 4 | `source .venv/bin/activate && uvicorn app.main:app --app-dir services/sensor-orchestrator --host 0.0.0.0 --port 8100 --reload` | Starts the FastAPI service |

### 7. Validate the core flow

Check health and pricing first, then verify the central commercial mechanic: an unpaid first request should return **HTTP 402**, while a properly authorized retry should complete successfully.

### 8. Security and publishing posture

Before any public push, confirm that GitHub governance is enabled. GitHub documents branch protection, required reviews, status checks, and secure build practices as foundational controls for public repositories and growing teams [1] [2].

### 9. Founder profile publication

GitHub can display a profile README when a public repository matches the username. For `psycall`, that means a public repository named `psycall` containing the prepared `README.md` [3]. The starter materials live in `profile/`.

### 10. Executive launch checklist

Before showing the project to partners, judges, or investors, confirm the repository is not only functional but also publicly convincing.

## References

[1]: https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository "GitHub Docs — Quickstart for securing your repository"
[2]: https://docs.github.com/en/code-security/tutorials/implement-supply-chain-best-practices/securing-builds "GitHub Docs — Securing builds"
[3]: https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme "GitHub Docs — Managing your profile README"
