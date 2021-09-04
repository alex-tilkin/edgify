import os


class FilesStorage:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def save(self, uploaded_file):
        file_path = os.path.join(self.upload_folder, uploaded_file.filename)
        uploaded_file.save(file_path)

        return file_path
