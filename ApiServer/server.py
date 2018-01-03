from flask import Flask, render_template, request
import base64
from os import path
import numpy as np
import pymongo
from SessionFactory import SessionRunnerFactory
import json
app = Flask(__name__)

client = pymongo.MongoClient('localhost', 27017)
db = client.tensormarket
models = db.models

RunnerPool = {}

@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


def getModelRunner(model):
    model_key = (model['author'], model['name'])
    if model_key not in RunnerPool:
        models_dir = "../models"
        model_dir = path.join(models_dir, model['author'], model['name'])

        input_labels = map(lambda x: x["name"], model["input_tensors"])
        output_labels = map(lambda x: x["name"], model["output_tensors"])

        runner = SessionRunnerFactory().getRunner(model_dir, model["name"], model["signature_key"], input_labels,
                                                  output_labels)
        RunnerPool[model_key] = runner
    return RunnerPool[model_key]

def decodeInputData(data):
    decoded_data = {}
    for label in data:
        ori = data[label]
        buf = base64.decodestring(ori)
        decoded_data[label] = [np.frombuffer(buf, dtype=np.float32)]
    return decoded_data


def outputToJson(data):
    rval = {}
    for key in data.keys():
        rval[key] = data[key].tolist()
    return json.dumps(rval)


@app.route('/consume/<author>/<model_name>', methods=['POST'])
def consume(author, model_name):
    model = models.find_one({"author": author, "name": model_name})

    runner = getModelRunner(model)
    input_data = decodeInputData(request.get_json(force=True))

    result = runner.run(input_data)

    return outputToJson(result)


if __name__ == '__main__':
    app.run(debug=True)