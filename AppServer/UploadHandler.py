import zipfile, os


class UploadHandler:
    def __init__(self, directory, database):
        pass

    def saveModel(self, file, input_labels, output_labels):
        pass

    def saveZip(self, ??):
        pass

    def extractModel(self, path_to_zip_file, directory_to_extract_to):
        zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
        zip_ref.extractall(directory_to_extract_to)
        zip_ref.close()
        os.remove(path_to_zip_file)

    def saveMetaDataToDB(self):
        db.save(username, modelname, signatuename, inputLaels, outputlabels)

