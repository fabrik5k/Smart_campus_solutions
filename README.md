
# Projeto gRPC + Kafka para Sensores

Este projeto implementa um serviço gRPC para recebimento de dados de sensores e publica esses dados em um tópico Kafka.

## Estrutura de Diretórios

```
.
├── docker-compose.yml        # Orquestração dos containers (Kafka, Zookeeper, etc.)
├── kafka_producer.py         # Cliente Kafka usado pelo servidor gRPC
├── proto/
│   └── sensor.proto          # Definição do serviço gRPC e mensagens
├── requirements.txt          # Dependências do projeto
├── sensor_pb2.py             # Código gerado pelo compilador protobuf
├── sensor_pb2_grpc.py        # Código gRPC gerado
└── server.py                 # Servidor gRPC
```

## Descrição do Funcionamento

1. **gRPC Server** (`server.py`):
   - Expõe o método `SendSensorData`.
   - Recebe dados dos sensores via gRPC.
   - Encaminha os dados ao Kafka utilizando o `kafka_producer.py`.

2. **Kafka Producer** (`kafka_producer.py`):
   - Conecta-se ao broker Kafka definido em `172.17.0.1:9092`.
   - Publica os dados no tópico `sensor-data`.

3. **Protobuf**:
   - Arquivo `proto/sensor.proto` define as mensagens `SensorRequest` e `SensorResponse` e o serviço `SensorService`.

## Como Executar

### 1. Clonar o repositório

```bash
git clone <seu-repositorio>
cd <pasta-do-projeto>
```

### 2. Subir os containers com Kafka

```bash
docker-compose up -d
```

### 3. Gerar arquivos a partir do .proto (se necessário)

```bash
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/sensor.proto
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Rodar o servidor gRPC

```bash
python server.py
```

## Exemplo de Requisição gRPC

Você pode usar um cliente gRPC Python ou ferramentas como Postman (com gRPC beta) para enviar uma requisição com o seguinte payload:

```json
{
  "sensor_id": "sensor-001",
  "type": "temperatura",
  "value": 26.5,
  "timestamp": "2025-04-24T00:00:00Z"
}
```

## Observações

- Certifique-se que o endereço IP e a porta do Kafka (`172.17.0.1:9092`) estão acessíveis no seu ambiente.
- Você pode alterar o endereço no arquivo `kafka_producer.py` se necessário.

---

Desenvolvido como parte de um projeto de integração entre gRPC e sistemas distribuídos com Kafka.
