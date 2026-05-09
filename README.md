# ORVION - The Agentic Settlement Layer

## Visão Geral

ORVION é uma camada de liquidação agêntica que facilita transações e coordenação entre agentes autônomos. Este projeto foi reestruturado para focar em uma arquitetura unificada e segura baseada em Python (FastAPI), garantindo escalabilidade, eficiência e robustez. Nosso objetivo é fornecer uma plataforma confiável para a orquestração de agentes, gerenciamento de liquidações e integração com redes blockchain como a Arc Network.

## Principais Características

- **API RESTful com FastAPI**: Uma API moderna e de alto desempenho para gerenciamento de agentes, liquidações e usuários.
- **Gerenciamento de Agentes**: Registro, descoberta e monitoramento de agentes autônomos com capacidades e modelos de precificação definidos.
- **Processamento de Liquidações**: Criação, rastreamento e processamento de liquidações, com suporte para histórico de transações.
- **Autenticação e Autorização Seguras**: Sistema de autenticação baseado em JWT com tokens de acesso e refresh, e gerenciamento de usuários.
- **Integração com Blockchain (Arc Network)**: Suporte para interação com a Arc Network para operações de liquidação e gerenciamento de ativos (e.g., USDC).
- **Monitoramento e Estatísticas**: Endpoints de dashboard para visualizar estatísticas da rede, desempenho de agentes e tendências de liquidação.
- **Configuração Centralizada e Segura**: Gerenciamento de configurações sensíveis via variáveis de ambiente, eliminando segredos hardcoded.

## Estrutura do Projeto

O projeto ORVION agora é centrado em um backend Python com FastAPI, eliminando as implementações redundantes em Node.js e Java para garantir uma base de código mais coesa e segura.

```
ORVION/
├── .env                      # Variáveis de ambiente (NÃO commitar segredos!)
├── main.py                   # Aplicação FastAPI principal
├── requirements.txt          # Dependências Python
├── auth_routes.py            # Rotas de autenticação e autorização
├── user_management_routes.py # Rotas de gerenciamento de usuários
├── settlements_history_routes.py # Rotas de histórico de liquidações
├── dashboard_stats_routes.py # Rotas de estatísticas do dashboard
├── orvion/
│   ├── __init__.py
│   ├── agent_registry.py     # Lógica de CRUD para agentes
│   ├── auth.py               # Funções de autenticação (hashing, JWT)
│   ├── config.py             # Configurações da aplicação
│   ├── database.py           # Configuração do banco de dados (SQLAlchemy)
│   ├── models.py             # Modelos de dados (SQLAlchemy ORM)
│   ├── schemas.py            # Schemas de validação (Pydantic)
│   └── settlement_engine.py  # Lógica de processamento de liquidações
├── docs/                     # Documentação adicional
│   ├── ARCHITECTURE.md       # Documentação da arquitetura
│   └── SECURITY.md           # Documentação de segurança
└── tests/                    # Testes da aplicação
```

## Configuração e Instalação

### Pré-requisitos

- Python 3.9+
- PostgreSQL (recomendado para produção) ou SQLite (para desenvolvimento)
- Redis (opcional, para caching ou filas)
- Neo4j (opcional, para grafos de relacionamento de agentes)

### Passos de Instalação

1.  **Clonar o Repositório**:
    ```bash
    git clone https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer.git
    cd ORVION-The-Agentic-Settlement-Layer
    ```

2.  **Configurar o Ambiente Virtual**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar Dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variáveis de Ambiente**:
    Crie um arquivo `.env` na raiz do projeto com base no `.env.example` fornecido. **Certifique-se de substituir os valores de `SECRET_KEY`, `NEO4J_PASSWORD`, `CIRCLE_API_KEY` e `CIRCLE_ENTITY_SECRET` por valores seguros e únicos em produção.**
    ```ini
    # Exemplo de .env
    PROJECT_NAME="ORVION - The Agentic Settlement Layer"
    PROJECT_VERSION="2.0.0"

    DATABASE_URL="postgresql://user:password@host:port/dbname" # Ou sqlite:///./orvion.db para desenvolvimento
    REDIS_URL="redis://localhost:6379/0"
    NEO4J_URI="bolt://localhost:7687"
    NEO4J_USER="neo4j"
    NEO4J_PASSWORD="your_neo4j_password"

    ARC_RPC_URL="https://testnet-rpc.arc.network"
    USDC_CONTRACT="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    ARC_CHAIN_ID="2602"

    SECRET_KEY="your_super_secret_key_for_jwt"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    CIRCLE_API_KEY="your_circle_api_key"
    CIRCLE_ENTITY_SECRET="your_circle_entity_secret"
    CIRCLE_ENV="sandbox"
    ```

5.  **Inicializar o Banco de Dados**:
    ```bash
    python -c "from orvion.database import init_db; init_db()"
    ```

6.  **Executar a Aplicação**:
    ```bash
    uvicorn main:app --reload
    ```
    A API estará disponível em `http://127.0.0.1:8000`.
    A documentação interativa (Swagger UI) estará em `http://127.0.0.1:8000/api/v1/openapi.json`.

## Uso

Consulte a documentação da API em `/api/v1/openapi.json` para detalhes sobre os endpoints disponíveis e como interagir com eles. Os endpoints de autenticação (`/api/v1/auth/signup`, `/api/v1/auth/login`) são os pontos de entrada para obter tokens de acesso.

## Contribuição

Contribuições são bem-vindas! Por favor, siga as diretrizes de contribuição (a ser definida) e o código de conduta.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido por Manus AI**
