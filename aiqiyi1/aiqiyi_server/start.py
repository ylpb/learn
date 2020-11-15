import sys
from conf import settings
from tcp_server import tcp_server



sys.path.append(settings.BASE_PATH)
if __name__ == '__main__':
    tcp_server.run()