# Pocket Oracle

![Pocket Oracle Hero Visual](public/brand/pocket-oracle-hero-annk-banana.png)

> Visual principal do projeto para README, pitch público e primeira impressão do repositório.

**PT-BR** | [**English Version**](README.en.md)

**Pocket Oracle** transforma qualquer smartphone em um **oráculo monetizável do mundo real para agentes de IA**, combinando verificação humana, sinais contextuais e cobrança por uso em um fluxo pronto para demonstração, validação técnica e evolução para micropagamentos machine-to-machine.

> A tese do projeto é direta: quando um agente precisa de uma confirmação do mundo físico, ele não deveria esperar por integrações lentas, processos manuais longos ou operações caras. Ele deveria pagar centavos, receber uma resposta verificável e continuar sua execução quase em tempo real.

## Visão executiva

Este repositório foi estruturado para parecer e operar como **startup séria**, não como protótipo improvisado. A base atual apresenta uma arquitetura de monorepo orientada a produto, com separação clara entre monetização, interfaces de operação, serviços de campo, contratos compartilhados, documentação estratégica, branding e controles de governança.

| Camada | Diretório | Papel estratégico |
| --- | --- | --- |
| Gateway pago | `apps/api-gateway` | Implementa o fluxo comercial e o comportamento `402 Payment Required` |
| Operação mobile | `apps/mobile-pwa` | Leva a experiência para smartphone, o centro do produto |
| Inteligência operacional | `apps/admin-dashboard` | Organiza métricas, estado da demo e visão executiva |
| Serviços de campo | `services/sensor-orchestrator` | Entrega OCR, geoproof e verificações humanas em FastAPI |
| Contratos e SDK | `packages/*` | Reduz acoplamento e acelera integrações buyer-side |
| Infra local | `infra/docker` | Sustenta banco, fila e ambiente previsível de evolução |
| Marca | `public/brand` | Consolida identidade visual premium para README, pitch e produto |
| Governança | `.github`, `SECURITY.md`, `CODEOWNERS` | Reforça disciplina operacional e confiança pública |

## O que o produto oferece agora

A versão atual já cobre o esqueleto funcional necessário para uma demonstração com narrativa econômica forte e potencial claro de produto.

| Serviço | Endpoint | Preço sugerido | Resultado esperado |
| --- | --- | ---: | --- |
| GeoProof | `POST /oracle/geoproof` | `0.0015` | Evidência contextual de localização |
| SnapOCR | `POST /oracle/snap-ocr` | `0.0040` | Extração curta de texto em ambiente real |
| HumanTap Verify | `POST /oracle/human-tap-verify` | `0.0060` | Confirmação humana rápida e auditável |

O gateway já demonstra o comportamento comercial central do produto: a primeira chamada sem autorização de pagamento retorna **HTTP 402**, o buyer assina ou envia a autorização correspondente, repete a chamada, e recebe a resposta do serviço imediatamente. Esse padrão torna a demo mais convincente para narrativas de cobrança por uso, automação agentic e marketplaces de microserviços físicos.

## Por que este repositório chama atenção

O objetivo não é somente “rodar”. O objetivo é fazer empresas, jurados, parceiros e desenvolvedores **entenderem rapidamente o valor**, sentirem confiança na execução e enxergarem espaço real de expansão.

| Frente | O que já existe | Valor percebido |
| --- | --- | --- |
| Narrativa | README executivo, roadmap, arquitetura e checklist | Explica o produto com clareza para públicos técnicos e de negócio |
| Segurança | Política de segurança, hardening, scanning e higiene de segredos | Reduz sinais de amadorismo e aumenta confiança pública |
| Produto | Monorepo com apps, serviços, SDK e contratos | Mostra visão arquitetural de longo prazo |
| Visual | Logo, ícone, tokens e arte premium gerada | Aumenta impacto na primeira impressão |
| Operação | Docker, scripts e base de build validada | Facilita onboarding e evolução do time |
| Governança | Templates, revisão e ownership | Aproxima o projeto de padrão profissional de engenharia |

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

A base foi organizada para permitir uma evolução rápida em ambiente local, mantendo previsibilidade operacional.

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

## Documentação principal

A documentação foi pensada como material de operação e também como ativo de credibilidade pública.

| Documento | Finalidade |
| --- | --- |
| [`SETUP.md`](SETUP.md) | Guia bilíngue de instalação, execução local, governança e preparo de demo |
| [`ROADMAP.md`](ROADMAP.md) | Roadmap executivo com as fases atuais e futuras do produto |
| [`docs/architecture.md`](docs/architecture.md) | Explica o desenho técnico do produto |
| [`docs/roadmap.md`](docs/roadmap.md) | Organiza a evolução por fases de negócio e engenharia |
| [`docs/submission-checklist.md`](docs/submission-checklist.md) | Estrutura a prontidão para demo e submissão |
| [`docs/github-hardening.md`](docs/github-hardening.md) | Detalha controles de segurança e governança no GitHub |
| [`docs/release-readiness.md`](docs/release-readiness.md) | Resume o estado validado da base atual |
| [`docs/ultra-hardening-and-profile-plan.md`](docs/ultra-hardening-and-profile-plan.md) | Define a próxima camada premium de posicionamento |
| [`docs/founder-launch-playbook.md`](docs/founder-launch-playbook.md) | Traz o passo a passo executivo para posicionar o projeto como startup premium |
| [`docs/brand-system.md`](docs/brand-system.md) | Documenta a identidade visual premium e as regras de uso da marca |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | Define padrões de colaboração e comportamento profissional |
| [`README.en.md`](README.en.md) | Apresenta a versão completa em inglês para parceiros e público internacional |

## Segurança e higiene operacional

Qualquer segredo exposto deve ser tratado como **comprometido imediatamente**. O fluxo correto é revogar, regenerar, limitar escopo e encurtar expiração. O GitHub recomenda ativar controles como branch protection, revisão obrigatória, secret scanning e práticas de build seguro para fortalecer repositórios e cadeias de build públicas [1] [2].

| Regra | Padrão recomendado |
| --- | --- |
| Credenciais expostas | Revogar imediatamente |
| Branch principal | `main` protegida |
| Alterações sensíveis | Revisão obrigatória |
| Workflows | Permissões mínimas |
| Dependências | Auditoria e atualização contínuas |

## Roadmap executivo

O projeto já comunica potencial de mercado no presente, mas também foi estruturado para crescimento claro em fases sucessivas. A versão executiva detalhada do roadmap está em [`ROADMAP.md`](ROADMAP.md).

| Fase | Objetivo | Resultado |
| --- | --- | --- |
| Fase 1 | Travar demo funcional | PWA, gateway, orquestrador e dashboard operando juntos |
| Fase 2 | Conectar liquidação real | Integração com wallet, settlement e prova auditável |
| Fase 3 | Tornar submission-grade | Deploy, narrativa pública, vídeo, slides e métricas |
| Fase 4 | Evoluir para produto real | Marketplace multi-device, reputação, SLA e roteamento |

## Próximas oportunidades de produto

A mesma infraestrutura conceitual pode evoluir para múltiplos mercados onde agentes precisam de dados físicos confiáveis e rápidos.

| Vertical | Uso potencial |
| --- | --- |
| Retail compliance | Checagem de preço, estoque, execução e auditoria |
| Delivery verification | Prova de entrega e confirmação contextual |
| Field operations | Inspeção, presença e validação operacional |
| Agentic commerce | Microtarefas físicas para agentes autônomos |
| Proof-of-presence | Evidência rápida para workflows híbridos |

## Regras de Git recomendadas

A governança de Git foi organizada para passar seriedade desde o primeiro contato com o repositório.

| Tema | Padrão |
| --- | --- |
| Branch principal | `main` |
| Features | `feat/...` |
| Correções | `fix/...` |
| Operação e docs | `chore/...`, `docs/...` |
| Estilo de commit | `feat:`, `fix:`, `docs:`, `chore:` |
| Política crítica | Nunca fazer commit de `.env`, segredos ou credenciais |

## English summary

**Pocket Oracle** turns any smartphone into a **monetizable real-world oracle for AI agents**, combining human verification, contextual sensing, and usage-based billing in a repository designed to look credible to developers, partners, judges, and early adopters.

The current monorepo already includes a paid gateway, mobile-first interface, admin dashboard, FastAPI field orchestration service, shared contracts, starter SDK, local infrastructure, visual branding, documentation, and GitHub governance. The next strategic move is to deepen trust, public polish, and real settlement integration.

For the full English version, open [**README.en.md**](README.en.md).

## References

[1]: https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository "GitHub Docs — Quickstart for securing your repository"
[2]: https://docs.github.com/en/code-security/tutorials/implement-supply-chain-best-practices/securing-builds "GitHub Docs — Securing builds"
