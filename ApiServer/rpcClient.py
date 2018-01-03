import grpc
import RPC.ModelService_pb2
import RPC.ModelService_pb2_grpc

import numpy as np
import base64
import json


class ModelRunnerClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = RPC.ModelService_pb2_grpc.ModelRunnerStub(self.channel)

    def run(self, json_input_data):
        request = RPC.ModelService_pb2.JsonMsg(msg=json_input_data)
        response = self.stub.run(request)
        return response


def testModelRunnerClient():
    client = ModelRunnerClient()
    input_data = np.zeros([1, 784], dtype=np.float32)
    inputs = {"input": base64.b64encode(input_data)}
    inputs = json.dumps(inputs)
    print client.run(inputs)


if __name__ == '__main__':
    testModelRunnerClient()
