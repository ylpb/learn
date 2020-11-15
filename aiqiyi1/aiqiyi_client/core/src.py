from core import admin,user

func_dic = {
    '1':admin.admin_view,
    '2':user.user_view
}




def run():
    while True:
        print('''
        欢迎来到仿爱奇艺视频
             1.管理员界面
             2.用户界面
             q.退出
        ''')
        choice = input('请选择功能：').strip()
        if choice == 'q':
            break
        if choice not in func_dic:
            print('请输入正确的功能选项')
            continue
        func_dic[choice]()