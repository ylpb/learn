import os
IP = '127.0.0.1'
PORT = 6666

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
UPLOAD_FILE_PATH = os.path.join(BASE_PATH,'upload_file')
DOWNLOAD_FILE_PATH = os.path.join(BASE_PATH,'download_file')