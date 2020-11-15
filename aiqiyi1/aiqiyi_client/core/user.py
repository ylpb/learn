from tcp_client import tcp_client
from lib import common
from conf import settings
import os

user_info = {'cookies': None,
             'is_vip': None}


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
            'user_type': 'user',
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
            'user_type': 'user',
            'username': username,
            'password': password
        }
        back_dic = common.send_and_back_data(send_dic, client)
        if back_dic.get('flag'):
            user_info['cookies'] = back_dic.get('session')
            user_info['is_vip'] = back_dic.get('is_vip')
            print(back_dic.get('msg'))
            break
        else:
            print(back_dic.get('msg'))
            break


def check_movie(client):
    send_dic = {
        'type': 'get_movie_list',
        'cookies': user_info.get('cookies'),
        'movie_type': 'all'
    }
    back_dic = common.send_and_back_data(send_dic, client)
    if not back_dic.get('flag'):
        print(back_dic.get('msg'))

    else:
        for index, movie_name in enumerate(back_dic.get('movie_list')):
            print(index, movie_name)


def buy_vip(client):
    sure_buy = input('请确认是否购买vip(y/n):')
    if sure_buy == 'y':
        send_dic = {
            'type': 'buy_vip',
            'cookies': user_info.get('cookies'),
            'is_vip': 1
        }
        back_dic = common.send_and_back_data(send_dic, client)
        print(back_dic.get('msg'))


def download_free_movie(client):
    while True:
        send_dic = {
            'type': 'get_movie_list',
            'movie_type': 'free',
            'cookies': user_info.get('cookies')
        }
        back_dic = common.send_and_back_data(send_dic, client)
        if not back_dic.get('flag'):
            print(back_dic.get('msg'))
            break
        else:
            movie_list = back_dic.get('movie_list')
            for index, movie in enumerate(movie_list):
                print(index, movie)
            choice = input('请输入需要下载的电影编号：').strip()
            if not choice.isdigit():
                print('请输入数字')
                continue
            choice = int(choice)
            if choice not in range(len(movie_list)):
                print('请输入正确的编号')
                continue
            movie_name = movie_list[choice][0]
            send_dic = {
                'type': 'download_movie',
                'movie_name': movie_name,
                'cookies': user_info.get('cookies'),
                'is_vip': user_info.get('is_vip')
            }
            back_dic = common.send_and_back_data(send_dic, client)
            movie_size = back_dic.get('movie_size')
            movie_path = os.path.join(settings.DOWNLOAD_FILE_PATH, movie_name)
            with open(movie_path, 'wb') as f:
                num = 0
                while num < movie_size:
                    data = client.recv(1024)
                    f.write(data)
                    num += len(data)
            print('下载完成！')
            break


def download_pay_movie(client):
    while True:
        send_dic = {
            'type': 'get_movie_list',
            'movie_type': 'not_free',
            'cookies': user_info.get('cookies')
        }
        back_dic = common.send_and_back_data(send_dic, client)
        if not back_dic.get('flag'):
            print(back_dic.get('msg'))
            break
        else:
            movie_list = back_dic.get('movie_list')
            for index, movie in enumerate(movie_list):
                print(index, movie)
            choice = input('请输入需要下载的电影编号：').strip()
            if not choice.isdigit():
                print('请输入数字')
                continue
            choice = int(choice)
            if choice not in range(len(movie_list)):
                print('请输入正确的编号')
                continue
            if user_info.get('is_vip'):
                buy_movie = input('尊贵的会员，请确认是否购买此片(y/n)').strip()
                if not buy_movie == 'y':
                    print('支付失败')
                    break
            else:
                buy_movie = input('请确认是否购买此片(y/n)').strip()
                if not buy_movie == 'y':
                    print('支付失败')
                    break

            movie_name = movie_list[choice][0]
            send_dic = {
                'type': 'download_movie',
                'movie_name': movie_name,
                'cookies': user_info.get('cookies'),
                'is_vip': user_info.get('is_vip')
            }
            back_dic = common.send_and_back_data(send_dic, client)
            movie_size = back_dic.get('movie_size')
            movie_path = os.path.join(settings.DOWNLOAD_FILE_PATH, movie_name)
            with open(movie_path, 'wb') as f:
                num = 0
                while num < movie_size:
                    data = client.recv(1024)
                    f.write(data)
                    num += len(data)
            print('下载完成！')
            break


def check_download_record(client):
    send_dic = {
        'type': 'check_download_record',
        'cookies': user_info.get('cookies')
    }
    back_dic = common.send_and_back_data(send_dic, client)
    if not back_dic.get('flag'):
        print(back_dic.get('msg'))
    else:
        for i in enumerate(back_dic.get('record_list')):
            print(i)


def check_notice(client):
    send_dic = {
        'type': 'check_notice',
        'cookies': user_info.get('cookies')
    }
    back_dic = common.send_and_back_data(send_dic, client)
    if not back_dic.get('flag'):
        print(back_dic.get('msg'))
    else:
        for i in enumerate(back_dic.get('notice_list')):
            print(i)


func_dic = {
    '1': register,
    '2': login,
    '3': check_movie,
    '4': buy_vip,
    '5': download_free_movie,
    '6': download_pay_movie,
    '7': check_download_record,
    '8': check_notice
}


def user_view():
    client = tcp_client.get_client()
    while True:
        print('''
        1.注册
        2.登录
        3.查看电影
        4.充值VIP
        5.下载免费电影
        6.下载收费电影
        7.查看下载记录
        8.查看公告
        q.退出
        ''')
        choice = input('请选择功能：').strip()
        if choice == 'q':
            break
        if choice not in func_dic:
            print('请输入正确的功能选项')
            continue
        func_dic[choice](client)
