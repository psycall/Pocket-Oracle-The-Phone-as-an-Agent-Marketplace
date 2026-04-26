# Arquitetura

A arquitetura do Orvion foi desenhada para demonstrar, de forma executiva e técnica, como um smartphone pode operar como camada de coleta contextual para agentes de IA com monetização por requisição.

```mermaid
flowchart LR
  A[Buyer Agent] -->|Request| B[API Gateway]
  B -->|402 sem autorização| A
  A -->|Retry com pagamento| B
  B --> C[Sensor Orchestrator]
  C --> D[GeoProof]
  C --> E[SnapOCR]
  C --> F[HumanTap Verify]
  B --> G[(Postgres)]
  B --> H[(Redis)]
  I[Mobile PWA] --> B
  J[Admin Dashboard] --> B
```

## Camadas

| Camada | Responsabilidade |
| --- | --- |
| Gateway | Validar pagamento, precificar requests e expor contratos públicos |
| Orquestrador | Executar tarefas do mundo real e padronizar resposta |
| Frontends | Demonstrar captura mobile e visibilidade operacional |
| Dados | Registrar eventos, métricas, jobs e receipts |

## Decisões de arquitetura

O gateway é a peça de monetização e reputação do sistema. O orquestrador é mantido como serviço separado para permitir futura evolução para workers assíncronos, filas, reputação por dispositivo e múltiplos provedores de execução.
