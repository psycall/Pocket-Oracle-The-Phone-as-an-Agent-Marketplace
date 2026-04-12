# Pocket Oracle — Founder Launch Playbook

**Autor:** Manus AI  
**Idioma principal:** Português do Brasil, com termos operacionais em inglês quando necessário.

## Propósito

Este playbook foi criado para orientar a evolução do **Pocket Oracle** como se o projeto já estivesse entrando em uma fase de exposição pública séria. O foco não é apenas publicar código. O foco é construir **confiança**, elevar a **percepção de produto**, reduzir riscos operacionais e fazer com que parceiros, recrutadores, jurados, investidores e desenvolvedores enxerguem um projeto com **potencial real de startup**.

> Um repositório forte não convence apenas pela ideia. Ele convence pela combinação entre narrativa clara, disciplina de execução, segurança visível, design consistente e sinais de continuidade.

## Resultado esperado

Ao concluir os passos deste documento, o projeto deve transmitir a imagem de uma base técnica que já saiu do estágio de rascunho e entrou em um estágio de **programa de produto**.

| Frente | Meta prática | Sinal público gerado |
| --- | --- | --- |
| Segurança | Regras, revisão, segredos protegidos e automações mínimas | Projeto confiável para colaboração |
| Produto | README forte, docs coerentes e jornadas claras | Tese fácil de entender |
| Marca | Social preview, logo, ícones e narrativa visual | Primeira impressão memorável |
| Execução | CI, release readiness e runbooks | Time preparado para operar |
| Perfil fundador | Presença pessoal alinhada ao projeto | Mais credibilidade e autoridade |

## Etapa 1 — Travar a superfície pública do repositório

O primeiro movimento deve ser consolidar o que qualquer visitante vê nos primeiros segundos. Essa etapa costuma decidir se a pessoa continua explorando o projeto ou sai da página.

| Ação | Como fazer | Critério de qualidade |
| --- | --- | --- |
| Definir descrição do repositório | No GitHub, editar a descrição curta do projeto | Frase clara, objetiva e de alto valor percebido |
| Definir website, se houver | Apontar para landing page futura ou demo pública | Link funcional e coerente com o README |
| Ativar social preview | Usar `public/brand/pocket-oracle-social-preview.png` | Capa legível e premium |
| Fixar tópicos | Usar tags como `ai`, `agents`, `mobile`, `marketplace`, `oracles`, `payments` | Ajuda descoberta e posicionamento |
| Ajustar repositórios em destaque no perfil | Fixar Pocket Oracle no topo do perfil | Dá prioridade estratégica ao projeto |

## Etapa 2 — Elevar a segurança do GitHub

A segurança precisa ser visível e operacional. Não basta dizer que o projeto é sério; a conta pública precisa demonstrar que existem controles objetivos.

| Controle | Onde ativar | Recomendações |
| --- | --- | --- |
| Branch protection | `Settings > Branches` | Exigir PR, bloquear push direto e exigir checks |
| Secret scanning | `Settings > Security` | Manter ativo sempre que disponível |
| Dependabot alerts | `Settings > Security` | Ativar alertas e updates automáticos |
| Code scanning | `Security` ou workflows dedicados | Adicionar quando o escopo do produto crescer |
| Actions permissions | `Settings > Actions` | Limitar permissões padrão e exigir menor privilégio |

Sempre que uma credencial aparecer em conversa, arquivo ou commit, ela deve ser considerada **comprometida**. O fluxo profissional é revogar, regenerar, documentar o incidente e impedir reincidência.

## Etapa 3 — Refinar a narrativa do produto

A narrativa do Pocket Oracle precisa deixar claro que a proposta não é “um app qualquer com IA”. O projeto deve ser entendido como infraestrutura de **verificação do mundo físico para agentes econômicos de software**.

| Mensagem | Como expressar no repositório |
| --- | --- |
| Smartphone como oráculo | Explicar que o device vira sensor e executor econômico |
| IA agentic com custo por uso | Mostrar a lógica do `402 Payment Required` |
| Confiança auditável | Ligar verificação humana, geoproof e OCR ao fluxo de evidência |
| Produto escalável | Indicar evolução para marketplace e settlement real |
| Tese startup | Demonstrar que existe caminho para monetização e operação real |

## Etapa 4 — Preparar o projeto para olhar de empresa

Quando uma empresa ou parceiro avalia um repositório, geralmente procura sinais de maturidade além do código. Por isso, a camada de governança deve ser tão nítida quanto a técnica.

| Elemento | Estado desejado |
| --- | --- |
| `README.md` | Explica visão, valor, produto, arquitetura, quick start e roadmap |
| `README.en.md` | Replica a força da narrativa para público internacional |
| `SECURITY.md` | Define política de reporte e postura frente a incidentes |
| `CODEOWNERS` | Protege áreas sensíveis e sinaliza disciplina |
| `docs/release-readiness.md` | Comunica prontidão operacional |
| `docs/github-hardening.md` | Mostra que a segurança não é improvisada |

## Etapa 5 — Preparar a demo como ativo comercial

Uma demo boa não deve apenas “funcionar”. Ela precisa parecer um recorte inicial de algo que já pode se transformar em negócio.

| Componente | O que mostrar |
| --- | --- |
| Gateway | Primeira chamada sem autorização retornando `402` |
| Orquestrador | Resposta coerente de OCR, geoproof e verificação humana |
| PWA mobile | Experiência centrada em smartphone |
| Dashboard | Métricas e visibilidade operacional |
| Documentação | Caminho explícito entre demo atual e produto futuro |

## Etapa 6 — Organizar releases com disciplina

Mesmo antes do primeiro usuário real, vale tratar o projeto como software de alto potencial. Isso muda a percepção pública e melhora a execução do time.

| Passo | Ação prática |
| --- | --- |
| Versionamento | Criar releases com tags semânticas simples |
| Changelog | Resumir mudanças relevantes por entrega |
| Critério de merge | Só liberar para `main` com checks aprovados |
| Evidência | Associar release a docs, screenshots e resultados de validação |
| Pós-release | Registrar riscos, pendências e próximos passos |

## Etapa 7 — Transformar o perfil do fundador em extensão do produto

O perfil de `psycall` deve funcionar como continuação natural do Pocket Oracle. Ele não pode parecer genérico. Precisa comunicar construção de produto, ambição técnica e clareza de execução.

| Elemento do perfil | Direção recomendada |
| --- | --- |
| Headline | Builder of AI products, systems, and execution layers |
| Bio curta | Foco em IA aplicada, automação, arquitetura e produto mobile-first |
| Repositório em destaque | Pocket Oracle como flagship |
| Banner | Usar `public/brand/psycall-dev-banner.png` como referência visual |
| README de perfil | Narrativa curta, técnica e madura |

## Etapa 8 — Preparar próximos movimentos estratégicos

Depois da camada pública premium, o projeto deve entrar em uma sequência de expansão focada em mercado e prova técnica.

| Movimento | Prioridade | Resultado esperado |
| --- | --- | --- |
| Settlement real | Alta | Demonstração econômica mais forte |
| Landing page pública | Alta | Canal de apresentação para parceiros |
| Vídeo curto da demo | Média | Melhora compartilhamento e submissões |
| Métricas de uso | Média | Base para discurso de produto |
| Integrações buyer-side | Alta | Aproxima o projeto de casos reais |

## Checklist final do fundador

Antes de divulgar o projeto com força, a revisão final deve ser objetiva e rigorosa.

| Verificação | Estado esperado |
| --- | --- |
| README em PT-BR e inglês | Publicados e consistentes |
| Social preview | Ativo no GitHub |
| Branch protection | Ativada |
| Secrets antigos | Revogados |
| Workflows | Executando com sucesso |
| Docs de segurança e release | Atualizados |
| Perfil `psycall` | Coerente com o projeto |
| Repositório fixado | Sim |

## Conclusão

Se este playbook for seguido com consistência, o Pocket Oracle deixa de parecer apenas um experimento criativo e passa a se apresentar como **uma startup técnica com narrativa forte, identidade visual própria, disciplina operacional e caminho claro de evolução**. Esse é exatamente o tipo de percepção que abre portas para colaboração, contratação, investimento e atenção qualificada.
