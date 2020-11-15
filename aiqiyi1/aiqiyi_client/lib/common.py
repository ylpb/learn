import struct
import json
import hashlib
import os




def send_and_back_data(send_dic,client,file=None):
    send_dic_bytes = json.dumps(send_dic).encode('utf8')
    send_dic_len = len(send_dic_bytes)
    header = struct.pack('i',send_dic_len)
    client.send(header)
    client.send(send_dic_bytes)
    
    if file:
        with open(file,'rb') as f:
            for line in f:
                client.send(line)

    header_pack = client.recv(4)
    back_dic_len = struct.unpack('i', header_pack)[0]
    back_dic_bytes = client.recv(back_dic_len)
    back_dic = json.loads(back_dic_bytes.decode('utf8'))

    return back_dic

def get_movie_md5(file_path):
    movie_md5 = hashlib.md5()
    movie_size = os.path.getsize(file_path)
    size_list = [0,movie_size//4,movie_size//2,3*(movie_size//4),movie_size-10]
    with open(file_path,'rb') as f:
        for i in size_list:
            f.seek(i)
            movie_md5.update(f.read(10))

    return movie_md5.hexdigest()






