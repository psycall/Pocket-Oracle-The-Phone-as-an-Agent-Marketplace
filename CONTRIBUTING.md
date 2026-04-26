# Contribuindo para o Orvion

Bem-vindo ao **Orvion**! Agradecemos seu interesse em contribuir para este projeto inovador. Este guia detalha como você pode participar de forma eficaz, mantendo a qualidade, a segurança e a visão estratégica do nosso produto.

Nosso projeto é um monorepo de nível industrial, focado em **micropagamentos agentic e inteligência do mundo real**. Valorizamos contribuições que agreguem valor, sejam bem documentadas e sigam nossas diretrizes de engenharia e comunicação.

## 🤝 Como Contribuir

### 1. Entenda a Visão

Antes de começar, familiarize-se com a [Visão Executiva](README.md#%EF%B8%8F-visão-executiva), a [Arquitetura](README.md#%EF%B8%8F-arquitetura) e o [Roadmap Estratégico](README.md#%EF%B8%8F-roadmap-estratégico) do projeto. Isso garantirá que suas contribuições estejam alinhadas com nossos objetivos de longo prazo.

### 2. Encontre uma Tarefa

*   **Issues Existentes:** Verifique a seção de [Issues](https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/issues) para encontrar tarefas abertas, bugs ou melhorias propostas. Comente na issue que você pretende trabalhar nela para evitar duplicação de esforços.
*   **Novas Ideias:** Se você tem uma nova ideia ou encontrou um bug, por favor, abra uma nova issue descrevendo-o detalhadamente. Inclua:
    *   **Contexto:** Por que a mudança é necessária?
    *   **Justificativa:** Qual problema ela resolve ou qual valor agrega?
    *   **Impacto Esperado:** Como ela afeta o sistema ou os usuários?

### 3. Fluxo de Desenvolvimento

Seguimos um fluxo de trabalho baseado em branches e Pull Requests (PRs):

1.  **Fork** o repositório e clone-o para sua máquina local.
2.  Crie uma **branch** a partir da `main` com um nome descritivo, seguindo a convenção `tipo/breve-descricao` (ex: `feat/add-jwt-auth`, `fix/geoproof-bug`).
3.  Faça suas **alterações** no código, adicionando testes quando apropriado e atualizando a documentação se necessário.
4.  **Commit** suas alterações usando a [Convenção de Commits](#-convenção-de-commits).
5.  **Push** suas alterações para o seu fork.
6.  Abra um **Pull Request (PR)** para a branch `main` do repositório original.

## 📝 Convenção de Commits

Utilizamos a convenção [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) para manter um histórico de commits limpo e legível. Isso nos ajuda a gerar changelogs automaticamente e a entender o propósito de cada alteração.

**Formato:**

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

**Tipos Comuns:**

*   `feat`: Uma nova funcionalidade.
*   `fix`: Uma correção de bug.
*   `docs`: Alterações na documentação.
*   `style`: Mudanças que não afetam o significado do código (espaços em branco, formatação, ponto e vírgula ausente, etc.).
*   `refactor`: Uma mudança de código que não corrige um bug nem adiciona um recurso.
*   `perf`: Uma mudança de código que melhora o desempenho.
*   `test`: Adição de testes ausentes ou correção de testes existentes.
*   `chore`: Outras mudanças que não modificam arquivos `src` ou `test` (ex: atualizações de build, dependências).
*   `build`: Alterações que afetam o sistema de build ou dependências externas (escopos de exemplo: gulp, broccoli, npm).
*   `ci`: Alterações nos arquivos e scripts de configuração de CI (escopos de exemplo: Travis, Circle, BrowserStack, SauceLabs).

**Exemplos:**

```text
feat(auth): implementar autenticação JWT
fix(geoproof): corrigir cálculo de precisão do GPS
docs(readme): atualizar seção de roadmap
```

## ✅ Qualidade Mínima para Pull Requests

Para que seu PR seja aprovado e mergeado, ele deve atender aos seguintes critérios:

*   **Testes:** Novas funcionalidades devem vir acompanhadas de testes unitários e/ou de integração. Correções de bugs devem incluir testes de regressão.
*   **Documentação:** Atualize a documentação relevante (README, arquivos `docs/`, comentários no código) para refletir suas mudanças.
*   **Coerência:** A mudança deve ser coerente com a narrativa do produto e a visão estratégica do Orvion.
*   **Segurança:** Garanta que nenhuma credencial, chave de API ou informação sensível seja incluída no código ou nos commits. Siga as diretrizes de [Segurança e Governança](README.md#%EF%B8%8F-segurança-e-governança).
*   **Monetização:** Se a mudança afeta o fluxo de pagamento, verifique se ele permanece funcional e seguro.
*   **Revisão de Código:** Esteja preparado para receber feedback e iterar sobre suas mudanças. Nosso objetivo é a excelência técnica.

## 🛡️ Segurança

Se você encontrar uma vulnerabilidade de segurança, **NÃO** a reporte publicamente em issues ou PRs. Por favor, entre em contato diretamente com os mantenedores do projeto através de um canal privado para que possamos endereçar a questão de forma responsável.

## ❓ Dúvidas

Se tiver alguma dúvida sobre como contribuir, sinta-se à vontade para abrir uma issue ou entrar em contato. Estamos aqui para ajudar!

---

**Orvion © 2026**
