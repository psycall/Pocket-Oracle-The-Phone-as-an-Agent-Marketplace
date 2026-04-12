# Security Policy

**PT-BR** | **EN**

A segurança do **Pocket Oracle** parte de um princípio simples: **qualquer segredo exposto deve ser tratado como comprometido imediatamente**. Em um projeto que lida com infraestrutura, automação econômica, integração entre serviços e possível evolução para pagamentos programáticos, a confiança operacional depende tanto do código quanto da disciplina de publicação, build e governança.

| Área | Regra de base |
| --- | --- |
| Credenciais | Escopo mínimo, expiração curta e rotação imediata em caso de exposição |
| Branch principal | Proteção obrigatória com revisão e checks críticos |
| CI/CD | Permissões mínimas e dependências auditadas |
| Divulgação de falhas | Canal privado sempre que possível |
| Ambiente local | Apenas dados e credenciais de desenvolvimento |

## PT-BR

### Escopo da política

Esta política cobre o repositório público, workflows de automação, dependências, documentação operacional, credenciais de integração, ambiente local de desenvolvimento e qualquer ativo público associado à execução do projeto. O objetivo é reduzir risco de exposição, erro operacional e compromissos desnecessários de confiança.

### Relato responsável

Se você identificar uma vulnerabilidade, falha de autorização, exposição de segredo, comportamento inseguro em workflow ou risco de supply chain, reporte de forma privada ao mantenedor antes de abrir qualquer issue pública. Sempre que possível, inclua impacto, passos de reprodução, componentes afetados e evidências mínimas necessárias para análise.

### Baseline obrigatório

O projeto deve operar com uma linha de base de segurança explícita, não implícita.

| Controle | Padrão esperado |
| --- | --- |
| Tokens e chaves | Fine-grained quando possível, escopo mínimo e expiração curta |
| Segredos | Nunca em commits, screenshots, issues, chats, PRs ou documentação pública |
| `main` | Protegida contra alterações diretas não revisadas |
| Pull requests sensíveis | Revisão obrigatória antes de merge |
| Dependências | Alertas, atualização contínua e auditoria regular |
| Workflows | Permissões mínimas e actions confiáveis |
| Artefatos locais | Uso apenas para desenvolvimento e demonstração controlada |

### Procedimento para credencial exposta

Em caso de exposição, o procedimento padrão deve ocorrer sem exceções e na seguinte ordem: **revogar**, **regenerar**, **reduzir escopo**, **registrar o incidente**, **verificar histórico Git**, **auditar uso recente** e **atualizar automações afetadas**. Nenhuma credencial previamente exposta deve voltar a ser considerada segura.

| Etapa | Ação |
| --- | --- |
| 1 | Revogar imediatamente a credencial comprometida |
| 2 | Criar nova credencial com escopo mínimo |
| 3 | Definir expiração curta sempre que aplicável |
| 4 | Revisar logs, automações e usos recentes |
| 5 | Confirmar que a credencial antiga não está mais ativa |

### Segurança de repositório e governança

A camada pública do projeto deve manter branch protection em `main`, revisão obrigatória para mudanças sensíveis, status checks críticos, secret scanning, Dependabot alerts e exclusão automática de branches após merge. Essas medidas reduzem erro humano e elevam a confiança em repositórios públicos mantidos em ritmo de produto [1] [2].

### Segurança de build e supply chain

Toda cadeia de build deve seguir princípio de menor privilégio. Workflows devem declarar permissões mínimas, preferir actions conhecidas e manter revisão periódica de dependências. Mudanças em CI, automação, scripts de bootstrap e infraestrutura merecem atenção adicional porque podem ampliar superfície de ataque de forma silenciosa [2].

### Ambiente local e demonstrações

O ambiente local existe para desenvolvimento, validação e demonstração controlada. Ele não deve receber segredos de produção, carteiras reais sem necessidade explícita, credenciais compartilhadas entre pessoas ou dados que elevem indevidamente o impacto de um vazamento. Demonstrações públicas devem ser gravadas com cuidado para evitar exposição visual de chaves, URLs sensíveis, cabeçalhos de autorização ou histórico de terminal.

### Política de divulgação

Relatórios responsáveis devem priorizar redução de dano. Evite publicar exploração detalhada, segredos, payloads completos ou passos reprodutíveis publicamente antes de existir mitigação adequada. Quando a correção for concluída, a divulgação deve equilibrar transparência e prudência operacional.

## EN

### Policy scope

This policy covers the public repository, automation workflows, dependencies, operational documentation, integration credentials, local development environment, and any public asset associated with project execution. The goal is to reduce exposure risk, operational mistakes, and unnecessary trust failures.

### Responsible reporting

If you identify a vulnerability, authorization flaw, exposed secret, insecure workflow behavior, or supply-chain risk, report it privately to the maintainer before opening a public issue whenever possible.

### Required baseline

The project should operate with an explicit security baseline rather than an assumed one.

### Exposed credential procedure

If a credential is exposed, the default procedure is non-negotiable: **revoke**, **regenerate**, **reduce scope**, **record the incident**, **inspect Git history**, **audit recent use**, and **update affected automations**.

### Repository and governance security

The public repository should maintain protected `main`, required review for sensitive changes, mandatory status checks, secret scanning, Dependabot alerts, and automatic deletion of merged branches. These controls reduce human error and improve confidence in public product repositories [1] [2].

### Build and supply-chain security

The build chain should follow least-privilege principles. Workflows should declare minimal permissions, prefer trusted actions, and review dependencies regularly.

## References

[1]: https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository "GitHub Docs — Quickstart for securing your repository"
[2]: https://docs.github.com/en/code-security/tutorials/implement-supply-chain-best-practices/securing-builds "GitHub Docs — Securing builds"
