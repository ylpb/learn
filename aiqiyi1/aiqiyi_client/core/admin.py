from tcp_client import tcp_client
from lib import common
from conf import settings
import os

user_info = {'cookies':None}

def register(client):
    while True:
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        re_password = input('请确认密码：').strip()

        if not password == re_password:
            print('两次密码不一致')
            continue
        send_dic = {
            'type': 'register',
            'user_type': 'admin',
            'username': username,
            'password': password
        }
        back_dic = common.send_and_back_data(send_dic, client)
        if back_dic.get('flag'):
            print(back_dic.get('msg'))
            break
        else:
            print(back_dic.get('msg'))


def login(client):
    while True:
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()

        send_dic = {
            'type': 'login',
            'user_type': 'admin',
            'username': username,
            'password': password
        }
        back_dic = common.send_and_back_data(send_dic, client)
        if back_dic.get('flag'):
            user_info['cookies'] = back_dic.get('session')

            print(back_dic.get('msg'))
            break
        else:
            print(back_dic.get('msg'))
            break


def upload_movie(client):
    while True:
        movie_list_path = settings.UPLOAD_FILE_PATH
        movie_list = os.listdir(movie_list_path)
        if not movie_list:
            print('没有可上传的电影')
            break

        for index,movie in enumerate(movie_list):
            print(index,movie)
        choice = input('请选择需要上传的电影(q退出此功能)：').strip()
        if choice == 'q':
            break
        if not choice.isdigit():
            print('请输入数字')
            continue
        choice = int(choice)
        if choice not in range(len(movie_list)):
            print('请输入正确的编号')
            continue
        movie_name = movie_list[choice]
        movie_path = os.path.join(movie_list_path,movie_name)
        movie_md5 = common.get_movie_md5(movie_path)
        print(movie_md5)
        movie_size = os.path.getsize(movie_path)

        send_dic = {
            'type':'check_movie',
            'movie_md5':movie_md5,
            'cookies':user_info.get('cookies')
        }
        back_dic = common.send_and_back_data(send_dic,client)
        if not back_dic.get('flag'):
            print(back_dic.get('msg'))
            break
        print(back_dic.get('msg'))

        about_free = input('请确认是否免费(y/n)：')
        is_free = 0
        if about_free == 'y':
            is_free = 1
        send_dic = {
            'type':'upload_movie',
            'movie_name':movie_name,
            'movie_size':movie_size,
            'movie_md5':movie_md5,
            'is_free':is_free ,
            'cookies': user_info.get('cookies')
        }
        back_dic = common.send_and_back_data(send_dic,client,file=movie_path)
        print(back_dic.get('msg'))
        break


def delete_movie(client):
    while True:
        send_dic = {
            'type':'get_movie_list',
            'cookies': user_info.get('cookies'),
            'movie_type':'all'
        }
        back_dic = common.send_and_back_data(send_dic,client)
        if not back_dic.get('flag'):
            print(back_dic.get('msg'))
            break
        else:
            movie_list = back_dic.get('movie_list')
            if not movie_list:
                print('没有可删除的电影')
                break

            for index,movie in enumerate(movie_list):
                print(index,movie)
            choice = input('请选择需要删除的电影(q退出此功能)：').strip()
            if choice == 'q':
                break
            if not choice.isdigit():
                print('请输入数字')
                continue
            choice = int(choice)
            if choice not in range(len(movie_list)):
                print('请输入正确的编号')
                continue
            movie_name = movie_list[choice][0]
            send_dic = {
                'type':'delete_movie',
                'cookies': user_info.get('cookies'),
                'movie_name':movie_name
            }
            back_dic = common.send_and_back_data(send_dic,client)
            print(back_dic.get('msg'))
            break

def issue_notice(client):
    title = input('请输入标题：').strip()
    content = input('请输入内容：').strip()
    send_dic = {
        'type':'issue_notice',
        'cookies': user_info.get('cookies'),
        'title':title,
        'content':content
    }
    back_dic = common.send_and_back_data(send_dic,client)
    print(back_dic.get('msg'))


func_dic = {
    '1': register,
    '2': login,
    '3': upload_movie,
    '4': delete_movie,
    '5': issue_notice
}


def admin_view():
    client = tcp_client.get_client()
    while True:
        print('''
        1.注册
        2.登录
        3.上传电影
        4.删除电影
        5.发布公告
        ''')
        choice = input('请选择功能：').strip()
        if choice == 'q':
            break
        if choice not in func_dic:
            print('请输入正确的功能选项')
            continue
        func_dic[choice](client)
