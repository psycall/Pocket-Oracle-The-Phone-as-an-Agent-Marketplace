# Política de Segurança

A segurança do Pocket Oracle parte do princípio de que **qualquer segredo exposto deve ser tratado como comprometido imediatamente**. Isso inclui tokens de acesso, chaves de API, credenciais de banco, private keys e qualquer artefato que permita autenticação direta em serviços externos.

## Relato responsável

Se você identificar uma vulnerabilidade, um segredo exposto ou uma falha de autorização, reporte de forma privada ao mantenedor antes de abrir qualquer issue pública. O objetivo é reduzir janela de exploração e preservar a integridade do ambiente.

## Baseline obrigatório

| Controle | Regra |
| --- | --- |
| Tokens | Escopo mínimo e expiração curta |
| Secrets | Nunca em commits, screenshots, issues ou documentação |
| Branch principal | Protegida com revisão obrigatória |
| Dependências | Atualização contínua com alertas habilitados |
| Infra local | Apenas dados de desenvolvimento e testes |

## Rotação de credenciais

Em caso de exposição, o procedimento padrão deve seguir esta ordem: **revogar**, **gerar nova credencial**, **reduzir escopo**, **registrar incidente** e **verificar histórico Git para evitar persistência do vazamento**.
