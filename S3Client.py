import boto3
import os

class S3Client:
    def __init__(self, bucket_name, access_key_id, access_key):
        self.client = boto3.client(
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key,
        )
        self.bucket_name = bucket_name
        self.workdir = '/tmp'
        
    def uploadModel(self, username, model_name, local_path):
        self.client.upload_file(local_path, self.bucket_name, os.path.join(username, model_name))

    def downloadModel(self, username, model_name):
        # make path if not exist
        if os.path.isdir(os.path.join(self.workdir, username)):
            os.mkdir(os.path.join(self.workdir, username))

        key =  os.path.join(username, model_name)
        file_name = os.path.join(self.workdir, username, model_name) + ".zip"

        self.client.download_file(self.bucket_name, key, file_name)

def test():
    client = S3Client("tensormarket", ,)
    username = "pony"
    model_name = "mnist"
    local_path = "/Users/ChienliMa/Desktop/model10.ckpt.zip"
    # client.uploadModel(username, model_name, local_path)
    client.downloadModel(username, model_name)


test()