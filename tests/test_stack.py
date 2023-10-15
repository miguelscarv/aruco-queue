import grpc
import stack_pb2
import stack_pb2_grpc
import threading
import matplotlib.pyplot as plt

from PIL import Image
import PIL
import io

import json
import grpc
import time


def display_image(image):
    img = Image.open(io.BytesIO(image.data))
    ax = plt.gca()
    ax.imshow(img)
    plt.show()

def build_matrix(m):
    matrix = stack_pb2.Matrix()

    for row in m:
        matrix.row.add().elements.extend(row)

    return matrix

def test_add():

    TEST_MARTIX = [[0,0,0],
                   [1,1,1],
                   [2,2,2]]

    with grpc.insecure_channel("localhost:8061") as channel:
        stub = stack_pb2_grpc.StackServiceStub(channel)


        markers = []
        for id in range(3):
            R = build_matrix(TEST_MARTIX)
            t = build_matrix(TEST_MARTIX)
            corners = build_matrix(TEST_MARTIX)
            intrinsics = build_matrix(TEST_MARTIX)
            error = 1.23456
            
            mark = stack_pb2.Marker(R=R, t=t, corners=corners, intrinsics=intrinsics, id=str(id), error=error)
            markers.append(mark)
        
        res = stack_pb2.ImageData()
        res.markers.extend(markers)
        res.name = "test"
        res.is_last = False

        _ = stub.AddMarker(res)
        time.sleep(5)
        res.is_last = True
        _ = stub.AddMarker(res)


def test_get():
    with grpc.insecure_channel("localhost:8061") as channel:
        stub = stack_pb2_grpc.StackServiceStub(channel)

        try:
            
            res = stub.GetStack(stack_pb2.Empty())
            for m in res.images:
                print(m.is_last)
                

        except grpc.RpcError as rpc_error:
            print('An error has occurred in getting:')
            print(f'  Error Code: {rpc_error.code()}')
            print(f'  Details: {rpc_error.details()}')



if __name__ == "__main__":
    threading.Thread(target=test_add).start()
    threading.Thread(target=test_get).start()
    
