import boto3
import os


class S3Client:
    def __init__(self, access_key_id, access_key, bucket_name="tensormarket", work_dir="/tmp"):
        self.client = boto3.client(
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key,
        )
        self.bucket_name = bucket_name
        self.work_dir = work_dir
        
    def uploadModel(self, username, model_name, local_path):
        self.client.upload_file(local_path, self.bucket_name, os.path.join(username, model_name + ".zip"))

    def downloadModel(self, username, model_name):
        """
        :param username: author of this model
        :param model_name:  name of this model
        :effect get model zip from S3 by key username/model_name.zip and save at work_dir/username/model_name.zip
        :return: relative downloaded zipfile path
        """

        if not os.path.isdir(self.work_dir):
            os.mkdir(self.work_dir)

        if not os.path.isdir(os.path.join(self.work_dir, username)):
            os.mkdir(os.path.join(self.work_dir, username))

        key =  os.path.join(username, model_name + ".zip")
        local_file_name = os.path.join(self.work_dir, username, model_name) + ".zip"

        self.client.download_file(self.bucket_name, key, local_file_name)
        return local_file_name

def test(keyid, key):
    client = S3Client(keyid, key)
    username = "pony"
    model_name = "mnist"
    local_path = "/Users/ChienliMa/Desktop/model10.ckpt.zip"
    # client.uploadModel(username, model_name, local_path)
    client.downloadModel(username, model_name)

if __name__ == "__main__":
    access_key_id, access_key = sys.argv[1:]
    test(access_key_id, access_key )