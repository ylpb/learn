from db import models, session_data
from lib import common
import datetime
from threading import Lock

session_lock = Lock()


def register_interface(back_dic, conn):
    username = back_dic.get('username')
    password = back_dic.get('password')
    user_type = back_dic.get('user_type')
    user_obj_list = models.User.orm_select(username=username)
    if user_obj_list:
        send_dic = {'flag': False, 'msg': '用户名已存在'}
    else:
        user_obj = models.User(
            username=username,
            password=password,
            user_type=user_type,
            is_vip=0,
            register_time=datetime.datetime.now()
        )
        user_obj.orm_insert()
        send_dic = {'flag': True, 'msg': '注册成功'}
    common.send_data(send_dic, conn)


def login_interface(back_dic, conn):
    username = back_dic.get('username')
    password = back_dic.get('password')
    # user_type = back_dic.get('user_type')
    user_obj_list = models.User.orm_select(username=username)
    if not user_obj_list:
        send_dic = {'flag': False, 'msg': '用户名不存在'}
    else:

        user_obj = user_obj_list[0]
        print(user_obj.password)
        if user_obj.password != password:

            send_dic = {'flag': False, 'msg': '密码不正确'}
        else:
            session_lock.acquire()
            session = common.get_session()
            u_id = user_obj.u_id
            session_data.session_dic[back_dic.get('addr')] = [session, u_id]
            session_lock.release()

            send_dic = {'flag': True, 'msg': '登录成功', 'session': session}

    common.send_data(send_dic, conn)


@common.login_auth
def check_movie_interface(back_dic, conn):
    movie_md5 = back_dic.get('movie_md5')
    movie_obj_list = models.Movie.orm_select(file_md5=movie_md5)
    if movie_obj_list:
        send_dic = {'flag': False, 'msg': '该电影已上传'}
    else:
        send_dic = {'flag': True, 'msg': '可以上传'}
    common.send_data(send_dic, conn)


@common.login_auth
def get_movie_list_interface(back_dic, conn):
    movie_obj_list = models.Movie.orm_select(is_delete=0)
    # print(movie_obj_list)
    movie_type = back_dic.get('movie_type')
    movie_list = []
    if movie_obj_list:
        for movie_obj in movie_obj_list:

            if movie_type == 'all':
                movie_list.append([movie_obj.movie_name,
                                   '免费' if movie_obj.is_free == 1 else '收费'])
            elif movie_type == 'free':
                if movie_obj.is_free:
                    movie_list.append([movie_obj.movie_name, '免费'])
            else:
                if not movie_obj.is_free:
                    movie_list.append([movie_obj.movie_name, '收费'])
        if not movie_list:
            send_dic = {'flag': False, 'msg': '暂无电影可以下载'}
        else:
            send_dic = {
                'flag': True, 'movie_list': movie_list
        }
    else:
        send_dic = {'flag': False, 'msg': '暂无电影'}
    common.send_data(send_dic, conn)
