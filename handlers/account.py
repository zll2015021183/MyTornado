import tornado.web

from models.auth import register


class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html')

    def post(self):
        username = self.get_argument('username', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')

        if username and password1 and (password1 == password2):
            register(username, password1)
            self.write('注册成功！')
        else:
            self.write('用户名或者密码错误！')
