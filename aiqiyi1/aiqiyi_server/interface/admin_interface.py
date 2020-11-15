from conf import settings
from db import models
from lib import common
import os,datetime

@common.login_auth
def upload_movie_interface(back_dic,conn):
    movie_name = back_dic.get('movie_name')
    movie_size = back_dic.get('movie_size')
    movie_md5 = back_dic.get('movie_md5')
    is_free = back_dic.get('is_free')
    movie_path = os.path.join(settings.MOVIE_FILE_PATH,movie_name)
    num = 0
    with open(movie_path,'wb') as f:
        while num<movie_size:
            data = conn.recv(1024)
            f.write(data)
            num += len(data)
    movie_obj = models.Movie(
        movie_name=movie_name,
        movie_size=movie_size,
        movie_path=movie_path,
        is_free=is_free,
        u_id=back_dic.get('u_id'),
        file_md5=movie_md5,
        upload_time=datetime.datetime.now(),
        is_delete=0
    )
    movie_obj.orm_insert()
    send_dic = {'flag':True,'msg':'上传成功'}
    common.send_data(send_dic,conn)


@common.login_auth
def delete_movie_interface(back_dic,conn):

    movie_name = back_dic.get('movie_name')
    movie_obj_list = models.Movie.orm_select(movie_name=movie_name)
    movie_obj = movie_obj_list[0]
    movie_obj.is_delete = 1
    movie_obj.orm_update()
    send_dic = {'flag':True,'msg':'电影删除成功'}
    common.send_data(send_dic,conn)

@common.login_auth
def issue_notice_interface(back_dic,conn):
    title = back_dic.get('title')
    content = back_dic.get('content')
    notice_obj = models.Notice(
        title=title,
        content=content,
        create_time=datetime.datetime.now(),
        u_id=back_dic.get('u_id')
    )
    notice_obj.orm_insert()
    send_dic = {'flag':True,'msg':'公告发布成功'}
    common.send_data(send_dic,conn)