import socket
from conf import settings


def get_client():
    client = socket.socket()
    client.connect((settings.IP,settings.PORT))
    return client
