import json
import struct
import hashlib,uuid
from db import session_data


def send_data(send_dic,conn):
    send_dic_bytes = json.dumps(send_dic).encode('utf8')
    send_dic_len = len(send_dic_bytes)
    header = struct.pack('i', send_dic_len)
    conn.send(header)
    conn.send(send_dic_bytes)

def get_session():
    md5 = hashlib.md5()
    md5.update(str(uuid.uuid4()).encode('utf8'))
    return md5.hexdigest()


#print(get_session())

def login_auth(func):
    def inner(*args,**kwargs):
        user_session = args[0].get('cookies')
        addr = args[0].get('addr')
        if not session_data.session_dic:
            send_dic = {'flag': False, 'msg': '请先登录'}
            send_data(send_dic,args[1])
        else:
            server_session = session_data.session_dic.get(addr)[0]
            if user_session == server_session:
                args[0]['u_id'] = session_data.session_dic.get(addr)[1]
                res = func(*args,**kwargs)
                return res
            else:
                send_dic = {'flag':False,'msg':'请先登录'}
                send_data(send_dic, args[1])

    return inner

