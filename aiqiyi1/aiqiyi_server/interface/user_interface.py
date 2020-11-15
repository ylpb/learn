from db import models
from lib import common
from conf import settings
import datetime
import os


@common.login_auth
def buy_vip_interface(back_dic, conn):
    # is_vip = back_dic.get('is_vip')
    user_obj_list = models.User.orm_select(u_id=back_dic.get('u_id'))
    user_obj = user_obj_list[0]
    if user_obj.is_vip:
        send_dic = {
            'flag': False,
            'msg': '您已经是VIP，请勿重复购买！'
        }
    else:
        user_obj.is_vip = 1
        user_obj.orm_update()
        send_dic = {
            'msg': 'VIP会员购买成功！'
        }
    common.send_data(send_dic, conn)


@common.login_auth
def download_movie_interface(back_dic, conn):
    movie_name = back_dic.get('movie_name')
    movie_obj = models.Movie.orm_select(movie_name=movie_name)[0]
    m_id = movie_obj.m_id

    movie_path = os.path.join(settings.MOVIE_FILE_PATH, movie_name)
    movie_size = os.path.getsize(movie_path)
    send_dic = {
        'movie_size': movie_size
    }
    common.send_data(send_dic, conn)
    with open(movie_path, 'rb') as f:
        for line in f:
            conn.send(line)
    download_record_obj = models.DownloadRecord(
        m_id=m_id,
        u_id=back_dic.get('u_id'),
        download_time=datetime.datetime.now()
    )
    download_record_obj.orm_insert()


@common.login_auth
def check_download_record_interface(back_dic, conn):
    u_id = back_dic.get('u_id')
    record_obj_list = models.DownloadRecord.orm_select(u_id=u_id)
    record_list = []
    if not record_obj_list:
        send_dic = {
            'flag': False,
            'msg': '暂无下载记录'
        }
        common.send_data(send_dic, conn)
    else:
        for record_obj in record_obj_list:
            m_id = record_obj.m_id
            movie_obj = models.Movie.orm_select(m_id=m_id)[0]
            movie_name = movie_obj.movie_name
            record_list.append([movie_name, record_obj.download_time])
        send_dic = {'flag': True, 'record_list': record_list}
    common.send_data(send_dic, conn)


@common.login_auth
def check_notice_interface(back_dic, conn):
    notice_obj_list = models.Notice.orm_select()
    notice_list = []
    if not notice_obj_list:
        send_dic = {'flag': False, 'msg': '暂无公告'}

    else:
        for notice_obj in notice_obj_list:
            notice_list.append({'title': notice_obj.title,
                                'content': notice_obj.content,
                                'create_time': notice_obj.create_time})
        send_dic = {'flag': True, 'notice_list': notice_list}
    common.send_data(send_dic, conn)
