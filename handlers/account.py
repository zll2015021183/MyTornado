import tornado.web

from .main import BaseHandler
from util.account import authenticate


class RegisterHandler(tornado.web.RequestHandler, BaseHandler):
    def get(self):
        self.render('register.html')

    def post(self):
        username = self.get_argument('username', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')

        if username and password1 and (password1 == password2):
            self.orm.register(username, password1)
            self.write('注册成功！')
        else:
            self.write('用户名或者密码错误！')


class LoginHandler(BaseHandler):
    def get(self):
        next_url = self.get_argument('next', '')  # 获取next的值
        message = self.get_argument('message', '')
        self.render('login.html', message=message, next_url=next_url)

    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        next_url = self.get_argument('next', '')
        if not username.strip() or not password.strip():
            self.redirect('/login?message=用户名或密码为空')
        else:
            if authenticate(username, password):
                self.session.set('my_user', username)
                if next_url:
                    self.redirect(next_url)
                else:
                    self.redirect('/')
            else:
                self.redirect('/login?message=用户名或密码不正确')
