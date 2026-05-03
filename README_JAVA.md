# ORVION: The Agentic Settlement Layer

## Overview

ORVION is a decentralized settlement infrastructure for autonomous agents on Arc Network, powered by Circle USDC and built with Spring Boot + Web3j.

## Technology Stack

- **Backend:** Spring Boot 3.2.0 (Java 17)
- **Blockchain:** Web3j 4.10.0 (Arc Network Integration)
- **Database:** PostgreSQL 15
- **Cache:** Redis 7
- **Container:** Docker & Docker Compose
- **Build:** Maven 3.9.0

## Project Structure

```
orvion/
├── src/
│   ├── main/java/io/orvion/
│   │   ├── OrvionApplication.java
│   │   ├── api/
│   │   │   └── JobController.java
│   │   ├── service/
│   │   │   ├── JobService.java
│   │   │   ├── JobServiceImpl.java
│   │   │   ├── CircleIntegrationService.java
│   │   │   ├── ArcNetworkService.java
│   │   │   └── NanopaymentsService.java
│   │   ├── model/
│   │   │   └── Job.java
│   │   └── config/
│   ├── main/resources/
│   │   └── application.yml
│   └── test/java/io/orvion/
│       └── service/
│           └── JobServiceTest.java
├── pom.xml
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/
    └── java-ci.yml
```

## Quick Start

### Prerequisites
- Java 17+
- Maven 3.9.0+
- Docker & Docker Compose

### Local Development

1. **Clone repository:**
```bash
git clone https://github.com/psycall/orvion.git
cd orvion
```

2. **Setup environment:**
```bash
cp .env.testnet .env.local
export CIRCLE_API_KEY=your_key
export CIRCLE_ENTITY_SECRET=your_secret
```

3. **Build project:**
```bash
mvn clean install
```

4. **Run tests:**
```bash
mvn test
```

5. **Start application:**
```bash
mvn spring-boot:run
```

### Docker Deployment

1. **Build and run with Docker Compose:**
```bash
docker-compose up -d
```

2. **Access API:**
```
http://localhost:8080/api/v1/jobs
```

## API Endpoints

### Create Job
```bash
POST /api/v1/jobs
?creator=0x1234&worker=0x5678&amount=100.00&jobHash=hash123
```

### Complete Job
```bash
PUT /api/v1/jobs/{jobId}/complete
```

### Settle Job
```bash
PUT /api/v1/jobs/{jobId}/settle
```

### Get Job
```bash
GET /api/v1/jobs/{jobId}
```

### Get Agent Jobs
```bash
GET /api/v1/jobs/agent/{agentAddress}
```

### Get Pending Jobs
```bash
GET /api/v1/jobs/pending
```

## Configuration

Edit `src/main/resources/application.yml`:

```yaml
orvion:
  arc:
    rpc-url: https://testnet-rpc.arc.network
    chain-id: 2602
    contract-address: 0x...
  circle:
    api-key: your_api_key
    entity-secret: your_secret
  nanopayments:
    batch-size: 1000
    settlement-interval: 300
```

## Testing

```bash
# Run all tests
mvn test

# Run specific test
mvn test -Dtest=JobServiceTest

# With coverage
mvn test jacoco:report
```

## Building for Production

```bash
# Build JAR
mvn clean package

# Build Docker image
docker build -t orvion:1.0.0 .

# Push to registry
docker tag orvion:1.0.0 your-registry/orvion:1.0.0
docker push your-registry/orvion:1.0.0
```

## Deployment

### Arc Testnet

```bash
export ARC_RPC_URL=https://testnet-rpc.arc.network
export ARC_CHAIN_ID=2602
mvn spring-boot:run
```

### Arc Mainnet

```bash
export ARC_RPC_URL=https://mainnet-rpc.arc.network
export ARC_CHAIN_ID=2602
mvn spring-boot:run -Dspring-boot.run.arguments="--spring.profiles.active=production"
```

## Monitoring

Access metrics at:
```
http://localhost:8080/actuator
```

## Security

- Spring Security integrated
- JWT token support
- Rate limiting enabled
- Input validation on all endpoints
- CORS protection

## Support

- GitHub Issues: https://github.com/psycall/orvion/issues
- Documentation: https://docs.orvion.io
- Community: Discord [link]

## License

MIT
