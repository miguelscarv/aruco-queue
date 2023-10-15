import grpc 
import stack_pb2
import stack_pb2_grpc
import concurrent.futures as futures
import grpc_reflection.v1alpha.reflection as grpc_reflect
import time

DELAY = 2
_SERVICE_NAME = 'StackService'
VERBOSE = True

def print_data(request):
    print(f"File name: {request.name}")
    print(f"is_last: {request.is_last}")

class StackServer(stack_pb2_grpc.StackServiceServicer):

    def __init__(self) -> None:

        self.queue = []
        self.can_send = False

    def GetStack(self, request, context):

        while not self.can_send:
            time.sleep(DELAY)

        if VERBOSE:
            print("GETTING")
            print(f"Queue size: {len(self.queue)}")
            print("-----------------")

        self.can_send = False

        res = stack_pb2.ImagesData()
        res.images.extend(self.queue)
        self.queue = []
        
        return res

    def AddMarker(self, request, context):
        #print(request)
        self.queue.append(request)

        if request.is_last:
            self.can_send = True

        if VERBOSE:
            print("ADDING")
            print_data(request)
            print(f"Queue size: {len(self.queue)}")
            print("-----------------")

        return stack_pb2.Empty()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    stack_pb2_grpc.add_StackServiceServicer_to_server(
        StackServer(),
        server)

    SERVICE_NAME = (
        stack_pb2.DESCRIPTOR.services_by_name[_SERVICE_NAME].full_name,
        grpc_reflect.SERVICE_NAME
    )
    grpc_reflect.enable_server_reflection(SERVICE_NAME, server)
    server.add_insecure_port('[::]:8061')
    
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()