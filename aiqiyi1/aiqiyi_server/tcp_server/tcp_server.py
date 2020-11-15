import socket
import struct
import json
from interface import common_interface, user_interface, admin_interface
from conf import settings
from concurrent.futures import ThreadPoolExecutor
from db import session_data

pool = ThreadPoolExecutor(100)

server = socket.socket()
server.bind((settings.IP, settings.PORT))
server.listen(5)

func_dic = {
    'register': common_interface.register_interface,
    'login': common_interface.login_interface,
    'upload_movie': admin_interface.upload_movie_interface,
    'delete_movie': admin_interface.delete_movie_interface,
    'issue_notice': admin_interface.issue_notice_interface,
    'check_movie': common_interface.check_movie_interface,
    'get_movie_list': common_interface.get_movie_list_interface,
    'buy_vip': user_interface.buy_vip_interface,
    'download_movie': user_interface.download_movie_interface,
    'check_download_record':user_interface.check_download_record_interface,
    'check_notice': user_interface.check_notice_interface
}


def dispatcher(back_dic, conn):
    type = back_dic.get('type')
    if type in func_dic:
        func_dic[type](back_dic, conn)


def working(conn, addr):
    while True:
        try:
            header_pack = conn.recv(4)
            back_dic_len = struct.unpack('i', header_pack)[0]
            back_dic_bytes = conn.recv(back_dic_len)
            back_dic = json.loads(back_dic_bytes.decode('utf8'))
            back_dic['addr'] = addr
            dispatcher(back_dic, conn)
        except Exception as e:
            session_data.session_dic.pop(addr)
            print(e)
            break


def run():
    print('启动服务端')
    while True:
        conn, addr = server.accept()
        print(addr)
        pool.submit(working, conn, addr)
