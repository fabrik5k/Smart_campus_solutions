import time
import uuid
import random
import threading
from concurrent import futures

import grpc
from kafka import KafkaProducer
from google.protobuf.empty_pb2 import Empty

from sensor_pb2 import SyntheticData
from sensor_pb2_grpc import DataProducerServicer, add_DataProducerServicer_to_server

# CONFIGURAÇÕES
KAFKA_BOOTSTRAP = 'kafka:9092'
KAFKA_TOPIC = 'synthetic-data'
GRPC_PORT = 50051
INTERVAL_SECONDS = 1  # intervalo entre envios

class DataProducerService(DataProducerServicer):
    def __init__(self):
        # Inicializa o producer do Kafka com serialização Protobuf
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP,
            value_serializer=lambda msg: msg.SerializeToString()
        )

    def StreamData(self, request: Empty, context):
        while True:
            # Gera dados sintéticos
            msg = SyntheticData(
                timestamp=int(time.time() * 1000),
                measurement=random.random() * 100,
                id=str(uuid.uuid4())
            )

            # Publica no Kafka
            self.producer.send(KAFKA_TOPIC, msg)
            # opcional: block até a entrega
            # self.producer.flush()

            # Envia também pelo stream gRPC
            yield msg

            time.sleep(INTERVAL_SECONDS)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_DataProducerServicer_to_server(DataProducerService(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    server.start()
    print(f"gRPC server rodando na porta {GRPC_PORT} e enviando para Kafka em '{KAFKA_TOPIC}'")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Encerrando servidor...")

if __name__ == '__main__':
    serve()
