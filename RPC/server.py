from concurrent import futures
import time
import grpc
from ModelRunnerFactory import ModelRunnerFactory

import pymongo

import base64
import numpy as np
import json

import ModelService_pb2
import ModelService_pb2_grpc

import os
from os import path
import shutil
import zipfile

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ModelRunnerService(ModelService_pb2_grpc.ModelRunnerServicer):
    def __init__(self, runner):
        self.runner = runner

    def run(self, request, context):
        inputs = {}
        for input_label, input_data in json.loads(request.msg).iteritems():
            inputs[input_label] = [np.frombuffer(base64.decodestring(input_data), dtype=np.float32)]

        result = self.runner.run(inputs)

        for key in result.keys():
            result[key] = result[key].tolist()
        result = json.dumps(result)

        return ModelService_pb2.JsonMsg(msg=result)


def getCompressedModelFile(author, model_name, local_path = "./model"):
    remote_path = "../models"
    remote_path = path.join(remote_path, author, model_name + '.zip')

    if not os.path.isdir(local_path):
        os.mkdir(local_path)

    local_path = path.join(local_path,  model_name + '.zip')

    shutil.copy(remote_path, local_path)
    return local_path


def loadModelFile(author, model_name):
    local_path = "./model"

    # model files are stored as compressed zip file in remote file storage
    zip_file_path = getCompressedModelFile(author, model_name)

    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall(local_path)
    zip_ref.close()


def getModelRunner(author, model_name):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.tensormarket
    models = db.models
    model = models.find_one({"author": author, "name": model_name})
    client.close()

    models_dir = "./model"
    model_dir = path.join(models_dir, model['name'])

    input_labels = map(lambda x: x["name"], model["input_tensors"])
    output_labels = map(lambda x: x["name"], model["output_tensors"])

    runner = ModelRunnerFactory().getRunner(model_dir, model["name"], model["signature_key"], input_labels,
                                            output_labels)
    return runner


def serve(author, model_name):
    loadModelFile(author, model_name)
    getModelRunner(author, model_name)
    runner = getModelRunner(author, model_name)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ModelService_pb2_grpc.add_ModelRunnerServicer_to_server(ModelRunnerService(runner), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve("lol", "logistic_mnist_graph")
