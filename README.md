# Sensor Service

Este projeto implementa um serviço gRPC em Python que gera dados sintéticos periodicamente e os publica em um tópico Kafka.

## Estrutura de diretórios

```
.
├── proto/
│   └── sensor.proto
├── sensor_pb2.py
├── sensor_pb2_grpc.py
├── server.py
├── requirements.txt
├── Dockerfile.producer
└── docker-compose.yml
```

## Pré-requisitos

- Python 3.7+
- Kafka (rodando localmente ou em container, configurado em `docker-compose.yml`)
- `protoc` (Protocol Buffers Compiler)
- Docker & Docker Compose (opcional)

## Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repo>
   cd sensor-service
   ```
2. Crie um ambiente virtual e instale dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Gere os stubs gRPC:
   ```bash
   mkdir -p generated
   python -m grpc_tools.protoc -I./proto --python_out=./generated \
       --grpc_python_out=./generated proto/sensor.proto
   ```
4. Inicie o Kafka (via Docker Compose):
   ```bash
   docker-compose up -d
   ```

## Uso

1. Execute o servidor gRPC producer:
   ```bash
   python server.py
   ```
   O servidor ficará escutando na porta `50051` e publicando no tópico Kafka `synthetic-data` a cada segundo.

2. (Opcional) Teste o stream via um cliente gRPC Python:
   ```python
   from google.protobuf.empty_pb2 import Empty
   from sensor_pb2_grpc import DataProducerStub
   import grpc

   channel = grpc.insecure_channel('localhost:50051')
   stub = DataProducerStub(channel)
   for msg in stub.StreamData(Empty()):
       print(msg)
   ```

## Docker

Para empacotar o producer em um container Docker, use:

```bash
docker build -t sensor-producer -f Dockerfile.producer .
docker run --network host sensor-producer
```

## Licença

MIT
