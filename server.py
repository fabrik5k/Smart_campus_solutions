from concurrent import futures
import grpc
import sensor_pb2
import sensor_pb2_grpc
from kafka_producer import publish_sensor_data
from datetime import datetime

class SensorService(sensor_pb2_grpc.SensorServiceServicer):
    def SendSensorData(self, request, context):
        data = {
            "sensor_id": request.sensor_id,
            "type": request.type,
            "value": request.value,
            "timestamp": request.timestamp or datetime.utcnow().isoformat()
        }
        publish_sensor_data("sensor-data", data)
        return sensor_pb2.SensorResponse(status="OK")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_SensorServiceServicer_to_server(SensorService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("SensorService gRPC rodando na porta 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
