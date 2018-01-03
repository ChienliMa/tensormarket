import json
import requests
import base64
from os import path
import numpy as np

t = np.arange(25, dtype=np.float64)
s = base64.b64encode(t)
r = base64.decodestring(s)
q = np.frombuffer(r, dtype=np.float64)


class ApiClient:
    def __init__(self, url):
        self.url = url

    def postAsJson(self, url, payload):
        headers = {'content-type': 'application/json'}
        return requests.post(url, data=json.dumps(payload), headers=headers)

    def call(self, username, model_name, inputs):
        url = path.join(self.url, username, model_name)
        return self.postAsJson(url, inputs)


def test():
    input_data = np.zeros([1, 784], dtype=np.float32)
    inputs = {"input":base64.b64encode(input_data)}
    url = "http://localhost:5000/consume"
    client = ApiClient(url)
    print client.call("lol", "logistic_mnist_graph", inputs).text

if __name__ == "__main__":
    test()