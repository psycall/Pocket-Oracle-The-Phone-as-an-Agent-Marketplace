# GitHub Hardening Guide

Este guia resume a configuração recomendada para transformar o repositório do Orvion em um ativo público com padrão profissional, governança clara e menor risco operacional.

## Objetivo

A configuração abaixo protege a branch principal, reduz o risco de vazamento de segredos, melhora o fluxo de revisão e deixa o projeto preparado para colaboração séria, avaliação pública e futuras integrações contínuas.

| Área | Configuração recomendada | Motivo |
| --- | --- | --- |
| Branch protection | Proteger `main` | Evita alterações diretas não revisadas |
| Pull requests | Exigir revisão antes de merge | Eleva qualidade e governança |
| Status checks | Exigir workflows de CI e Security | Impede merge com build quebrado |
| Secret scanning | Habilitar detecção automática | Reduz risco de credenciais expostas |
| Dependabot alerts | Habilitar alertas e updates | Mantém dependências sob vigilância |
| Auto-delete branches | Ativar exclusão após merge | Mantém o repositório limpo |
| Default branch | Confirmar `main` | Padroniza fluxo de trabalho |

## Passo a passo

Primeiro, abra as configurações do repositório e navegue até a área de **Branches**. Crie uma regra de proteção para `main` exigindo pull request antes de merge, pelo menos uma aprovação, bloqueio de force push e exigência de resolução de conversas antes de concluir o merge.

Em seguida, na área de **Rules** ou **Branch protection**, marque os checks obrigatórios ligados aos workflows de qualidade e segurança. A intenção é garantir que apenas mudanças com build válido, auditoria básica de dependências e varredura de segredos possam entrar na branch principal.

Depois, vá para a seção de **Security** e habilite o máximo disponível do plano da conta, especialmente **secret scanning**, **Dependabot alerts**, **Dependabot security updates** e notificações de vulnerabilidades. Mesmo quando parte dos recursos avançados não estiver disponível, o baseline já melhora bastante a postura do projeto.

Por fim, confirme a seção de **General** para ativar exclusão automática de branches após merge e revisar se o repositório está com descrição, website, tópicos e social preview coerentes com a marca do produto.

## Descrição pública sugerida

> Orvion turns any smartphone into a monetizable real-world oracle for AI agents, powered by paid requests, mobile execution and micropayment-ready architecture.

## Tópicos sugeridos

| Grupo | Sugestões |
| --- | --- |
| Produto | `agentic-commerce`, `ai-agents`, `marketplace` |
| Infra | `monorepo`, `payments`, `fastapi`, `nextjs` |
| Narrativa | `micropayments`, `oracle`, `mobile`, `circle` |

## Regra operacional crítica

Se qualquer token, chave ou credencial for colado em chat, commit, issue, screenshot ou arquivo de configuração, trate imediatamente como comprometido. O procedimento certo é revogar, substituir, reduzir escopo e revisar o histórico antes de seguir.
