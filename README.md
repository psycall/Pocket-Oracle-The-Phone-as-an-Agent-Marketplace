# Pocket Oracle

**Pocket Oracle** transforma qualquer smartphone em um **oracle humano e contextual para agentes de IA**, com monetização por uso, prova de execução e trilha clara para micropagamentos machine-to-machine.

> A tese central do projeto é simples: quando um agente precisa de um dado do mundo físico, ele pode pagar centavos ou sub-centavos para obter uma resposta humana confiável, contextual e verificável.

## Visão executiva

O repositório foi estruturado para apresentar o projeto com padrão de **startup séria**, não como um MVP improvisado. A arquitetura está organizada em monorepo, com separação entre gateway de monetização, experiência mobile, painel executivo, orquestração de sensores, documentação de produto, branding e governança de engenharia.

| Bloco | Função | Valor estratégico |
| --- | --- | --- |
| `apps/api-gateway` | Gateway pago com resposta `402 Payment Required` | Demonstra monetização por requisição |
| `apps/mobile-pwa` | Interface mobile-first para operadores e buyers | Mostra uso prático em smartphone |
| `apps/admin-dashboard` | Painel de métricas e estado operacional | Fortalece narrativa de negócio |
| `services/sensor-orchestrator` | Serviço FastAPI para tarefas do mundo real | Base para OCR, geoproof e validação humana |
| `packages/agent-sdk` | SDK buyer-side para fluxo pay-and-retry | Acelera integrações futuras |
| `packages/shared-types` | Tipos e contratos compartilhados | Reduz drift entre serviços |
| `infra/docker` | Postgres e Redis locais | Base para persistência e fila |
| `public/brand` | Logo, ícone e tokens de marca | Aparência profissional e consistente |

## O que o produto oferece agora

O starter entrega o esqueleto funcional para uma demo de marketplace agentic com serviços pagos de alto valor narrativo.

| Serviço | Endpoint | Preço sugerido | Resultado |
| --- | --- | ---: | --- |
| GeoProof | `POST /oracle/geoproof` | `0.0015` | Evidência contextual de localização |
| SnapOCR | `POST /oracle/snap-ocr` | `0.0040` | Extração curta de texto em campo |
| HumanTap Verify | `POST /oracle/human-tap-verify` | `0.0060` | Confirmação humana rápida e rastreável |

O gateway já implementa o comportamento de demonstração mais importante para o pitch: a primeira chamada protegida responde com **HTTP 402**, a segunda chamada com autorização de pagamento é aceita, e a resposta do serviço é entregue imediatamente.

## Diferenciais do repositório

Este repositório já foi preparado para parecer ativo, seguro e escalável desde o primeiro contato de um investidor, jurado ou parceiro técnico.

| Frente | Entrega incluída |
| --- | --- |
| Branding | SVG de logo, ícone e tokens de marca |
| Governança | `CODEOWNERS`, templates de PR e issues, guia de contribuição |
| Segurança | `SECURITY.md`, `.gitignore`, baseline de segredos e rotação |
| Engenharia | monorepo com workspaces, apps, packages e docs |
| Operação | Docker Compose para Postgres e Redis |
| Demo | script para gerar carga de requisições pagas |
| Produto | roadmap com fases atual, próxima e expansão |

## Estrutura do monorepo

```text
.
├── apps/
│   ├── admin-dashboard/
│   ├── api-gateway/
│   └── mobile-pwa/
├── docs/
├── infra/
│   ├── docker/
│   └── scripts/
├── packages/
│   ├── agent-sdk/
│   └── shared-types/
├── public/
│   └── brand/
└── services/
    └── sensor-orchestrator/
```

## Quick start

A base foi pensada para permitir evolução rápida em ambiente local.

```bash
cp .env.example .env.local
npm install
docker compose -f infra/docker/docker-compose.yml up -d
npm run dev:api
```

Em outro terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r services/sensor-orchestrator/requirements.txt
uvicorn app.main:app --app-dir services/sensor-orchestrator --host 0.0.0.0 --port 8100 --reload
```

Para subir as interfaces:

```bash
npm run dev:mobile
npm run dev:admin
```

## Segurança e higiene operacional

Qualquer segredo exposto deve ser tratado como comprometido. O fluxo recomendado é **revogar, regenerar, limitar escopo e definir expiração curta**. Nunca faça commit de `.env`, credenciais de wallet, prints com segredos ou chaves em mensagens e documentação.

## Roadmap executivo

| Fase | Objetivo | Resultado esperado |
| --- | --- | --- |
| Fase 1 | Travar demo funcional | PWA + gateway + orquestrador + dashboard integrados |
| Fase 2 | Tornar Circle/Arc real | Liquidação real, hash e prova onchain |
| Fase 3 | Submission grade | Deploy, vídeo, slides e métricas públicas |
| Fase 4 | Produto de verdade | Marketplace multi-device, reputação e SLA |

## Regras de Git recomendadas

O repositório foi preparado para operar com convenção limpa de branches e commits.

| Tema | Padrão recomendado |
| --- | --- |
| Branch principal | `main` |
| Branches de feature | `feat/...` |
| Branches de correção | `fix/...` |
| Branches operacionais | `chore/...`, `docs/...` |
| Commit style | `feat:`, `fix:`, `docs:`, `chore:` |

## Próximas fases do produto

O potencial da plataforma vai além do hackathon. A mesma base pode evoluir para verificação de entrega, auditoria de campo, compliance em varejo, proof-of-presence e marketplaces regionais de microtarefas para agentes autônomos.

Consulte também [`docs/architecture.md`](docs/architecture.md), [`docs/roadmap.md`](docs/roadmap.md), [`docs/submission-checklist.md`](docs/submission-checklist.md), [`docs/github-hardening.md`](docs/github-hardening.md) e [`docs/release-readiness.md`](docs/release-readiness.md).
