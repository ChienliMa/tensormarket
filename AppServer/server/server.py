from flask import Flask, render_template, request
import zipfile, os
import pymongo

app = Flask(__name__)
app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

client = pymongo.MongoClient('localhost', 27017)
db = client.tensormarket


@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    model = {}
    form = request.form

    model["author"] = form["username"]
    model["name"] = form["model_name"]
    model["signature_key"] = form["signature_key"]

    f = request.files['file']
    f.save(f.filename)

    input_tensors = []
    i = 0
    while "input" + str(i) + "name" in form:
        input_tensor = {}
        input_tensor['name'] = form["input" + str(i) + "name"]
        input_tensor['width'] = int(form["input" + str(i) + "width"])
        input_tensor['height'] = int(form["input" + str(i) + "height"])
        input_tensor['datatype'] = form["input" + str(i) + "datatype"]
        input_tensor['description'] = form["input" + str(i) + "desc"]
        input_tensors.append(input_tensor)
        i += 1

    output_tensors = []
    i = 0
    while "input" + str(i) + "name" in form:
        output_tensor = {}
        output_tensor['name'] = form["output" + str(i) + "name"]
        output_tensor['width'] = int(form["output" + str(i) + "width"])
        output_tensor['height'] = int(form["output" + str(i) + "height"])
        output_tensor['datatype'] = form["output" + str(i) + "datatype"]
        output_tensor['description'] = form["output" + str(i) + "desc"]
        output_tensors.append(input_tensor)
        i += 1

    model["input_tensors"] = input_tensors
    model["output_tensors"] = output_tensors

    result = db.models.insert_one(model)
    print result

    zip_ref = zipfile.ZipFile(f.filename, 'r')
    zip_ref.extractall(os.path.join("../models/", model['author'],  model['name']))
    zip_ref.close()
    os.remove(f.filename)

    return 'file uploaded successfully'

if __name__ == "__main__":
    app.run()