from orm_client.orm import Models,IntegerField,StringField
class User(Models):
    u_id = IntegerField(name='u_id',primary_key=True)
    username = StringField(name='username')
    password = StringField(name='password')
    user_type = StringField(name='user_type')
    is_vip = IntegerField(name='is_vip')
    register_time = StringField(name='register_time')

class Movie(Models):
    m_id = IntegerField(name='m_id',primary_key=True)
    movie_name = StringField(name='movie_name')
    movie_size = IntegerField(name='movie_size')
    movie_path = StringField(name='movie_path')
    is_free = IntegerField(name='is_free')
    u_id = IntegerField(name='u_id')
    file_md5 = StringField(name='file_md5')
    upload_time = StringField(name='upload_time')
    is_delete = IntegerField(name='is_delete')

class Notice(Models):
    n_id = IntegerField(name='n_id',primary_key=True)
    title = StringField(name='title')
    content = StringField(name='content')
    create_time = StringField(name='create_time')
    u_id = IntegerField(name='u_id')

class DownloadRecord(Models):
    table_name = 'download_record'
    d_id = IntegerField(name='d_id',primary_key=True)
    m_id = IntegerField(name='m_id')
    u_id = IntegerField(name='u_id')
    download_time = StringField(name='download_time')


