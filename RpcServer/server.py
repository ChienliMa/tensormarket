from concurrent import futures
import time
import grpc

import ModelService_pb2
import ModelService_pb2_grpc

from ModelRunnerFactory import ModelRunnerFactory

from S3Client import S3Client

import pymongo

import base64
import numpy as np
import json

import os
import sys

import shutil
import zipfile


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

MODEL_DIR = "./model"

class ModelRunnerService(ModelService_pb2_grpc.ModelRunnerServicer):
    def __init__(self, runner):
        self.runner = runner

    def run(self, request, context):
        print "hit!!!"
        inputs = {}
        for input_label, input_data in json.loads(request.msg).iteritems():
            inputs[input_label] = [np.frombuffer(base64.decodestring(input_data), dtype=np.float32)]

        result = self.runner.run(inputs)

        for key in result.keys():
            result[key] = result[key].tolist()
        result = json.dumps(result)

        return ModelService_pb2.JsonMsg(msg=result)


def getCompressedModelFile(author, model_name, model_dir = MODEL_DIR):
    remote_path = "../models"
    remote_path = os.path.join(remote_path, author, model_name + '.zip')

    if not os.path.isdir(model_dir):
        os.mkdir(model_dir)

    local_path = os.path.join(model_dir,  model_name + '.zip')

    shutil.copy(remote_path, local_path)
    return local_path


def unZipModelFile(zip_file_path):
    """
    :param zip_file_path: relative path of zip file
    :return: nothing, extrace the file under MODEL_DIR
    """

    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall(MODEL_DIR)
    zip_ref.close()


def getModelRunner(model):
    model_dir = MODEL_DIR
    if os.path.isdir(os.path.join(model_dir, model["name"])):
        model_dir = os.path.join(model_dir, model["name"])

    input_labels = map(lambda x: x["name"], model["input_tensors"])
    output_labels = map(lambda x: x["name"], model["output_tensors"])

    runner = ModelRunnerFactory().getRunner(model_dir, model["name"], model["signature_key"], input_labels,
                                            output_labels)
    return runner


def serve(model):
    getModelRunner(model)
    runner = getModelRunner(model["author"], model["name"])

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ModelService_pb2_grpc.add_ModelRunnerServicer_to_server(ModelRunnerService(runner), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def getModelMeta(author, model_name, mongo_ip):
    client = pymongo.MongoClient(mongo_ip, 27017)
    db = client.tensormarket
    models = db.models
    model = models.find_one({"author": author, "name": model_name})
    client.close()
    return model


if __name__ == '__main__':
    if len(sys.argv) < 4:
        mongo_ip = "localhost"
        author, model_name = sys.argv[1:]
        zip_file_path = getCompressedModelFile(author, model_name)
    else:
        author, model_name, access_key_id, access_key, mongo_ip = sys.argv[1:]
        client = S3Client(access_key_id, access_key, work_dir=MODEL_DIR)
        zip_file_path = client.downloadModel(author, model_name)

    unZipModelFile(zip_file_path)

    model = getModelMeta(author, model_name, mongo_ip)
    serve(model)


