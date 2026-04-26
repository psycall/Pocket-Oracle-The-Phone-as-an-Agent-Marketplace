# Política de Segurança do Pocket Oracle

**PT-BR** | **EN**

No **Pocket Oracle**, a segurança é uma prioridade fundamental e um pilar estratégico do nosso desenvolvimento. Como um projeto que lida com micropagamentos, orquestração de agentes e dados do mundo real, a integridade, confidencialidade e disponibilidade do sistema são cruciais. Esta política descreve como abordamos a segurança, como relatar vulnerabilidades e as expectativas para todos os envolvidos no projeto.

## 🛡️ Nossas Prioridades de Segurança

Nós nos comprometemos a:

*   **Proteger Dados Sensíveis:** Garantir que informações de usuários, credenciais e dados operacionais sejam armazenados e processados de forma segura.
*   **Garantir a Integridade do Sistema:** Prevenir acessos não autorizados, modificações indevidas e interrupções de serviço.
*   **Manter a Confiança:** Construir e sustentar a confiança de nossos usuários e contribuidores através de práticas de segurança transparentes e eficazes.
*   **Resposta Rápida a Incidentes:** Ter um plano claro para identificar, mitigar e comunicar vulnerabilidades e incidentes de segurança.

## 🚨 Relatando uma Vulnerabilidade

Se você descobrir uma vulnerabilidade de segurança no **Pocket Oracle**, pedimos que a reporte de forma responsável e privada. **Por favor, NÃO divulgue vulnerabilidades publicamente (em issues, pull requests ou redes sociais) antes de nos dar a chance de corrigi-las.**

### Como Reportar:

1.  **Contato Direto:** Envie um e-mail para [security@pocketoracle.com] ou entre em contato com os mantenedores do projeto através de um canal privado (ex: mensagem direta no GitHub).
2.  **Informações Essenciais:** No seu relatório, inclua o máximo de detalhes possível:
    *   **Descrição:** Uma descrição clara e concisa da vulnerabilidade.
    *   **Passos para Reproduzir:** Instruções detalhadas sobre como reproduzir a vulnerabilidade.
    *   **Impacto:** O potencial impacto da vulnerabilidade (ex: vazamento de dados, execução remota de código).
    *   **Versão Afetada:** A versão ou commit do código onde a vulnerabilidade foi encontrada.
    *   **Proposta de Correção (Opcional):** Se você tiver uma sugestão de correção, por favor, inclua-a.

### Nosso Processo de Resposta:

1.  **Confirmação:** Iremos confirmar o recebimento do seu relatório em até 48 horas úteis.
2.  **Avaliação:** Nossa equipe de segurança avaliará a vulnerabilidade e seu impacto.
3.  **Mitigação:** Trabalharemos para desenvolver uma correção o mais rápido possível.
4.  **Divulgação:** Após a correção ser implementada e testada, faremos uma divulgação pública da vulnerabilidade e da solução, com os devidos créditos ao descobridor, se desejado.

## 🔒 Boas Práticas para Contribuidores

Todos os contribuidores são incentivados a seguir as melhores práticas de segurança:

*   **Higiene de Segredos:** Nunca faça commit de credenciais, chaves de API, arquivos `.env` ou qualquer informação sensível diretamente no repositório. Utilize variáveis de ambiente ou sistemas de gerenciamento de segredos.
*   **Revisão de Código:** Participe ativamente da revisão de código, buscando não apenas bugs funcionais, mas também potenciais falhas de segurança.
*   **Dependências:** Mantenha as dependências atualizadas e esteja ciente de vulnerabilidades conhecidas em bibliotecas de terceiros.
*   **Testes:** Inclua testes de segurança (quando aplicável) em suas contribuições.
*   **Princípio do Menor Privilégio:** Ao projetar ou implementar funcionalidades, sempre considere o princípio do menor privilégio.

## ⚖️ Licença

Este projeto é licenciado sob a [MIT License](LICENSE). Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença.

---

**Pocket Oracle © 2026**
