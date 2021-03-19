import grpc
from concurrent import futures
import time

# import the generated classes
import portao_pb2
import portao_pb2_grpc

class PortaoServicer(portao_pb2_grpc.PortaoServicer):

    def abrirPortao(self, request, context):
        response = portao_pb2.StatusPortao()
        # Vai apresentar ligada
        print(response)
        response.status = 1
        #print(self.request.temperatura)
        return response

    def fecharPortao(self, request, context):
        response = portao_pb2.StatusPortao()
        print(response)
        # -1 Vai representar desligada
        response.status = -1
        return response

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

portao_pb2_grpc.add_PortaoServicer_to_server(
        PortaoServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50053.')
server.add_insecure_port('[::]:50053')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)