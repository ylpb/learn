import sys
from core import src
from conf import settings



sys.path.append(settings.BASE_PATH)
if __name__ == '__main__':
    src.run()