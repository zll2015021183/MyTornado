import tornado.web
from tornado.options import define, options

# 自定义的模块
from handlers import main, account
from handlers.main import IndexHandler, ExploreHandler

# 定义端口信息
define('port', default='8000', help='listen port', type=int)
define('debug', default=True, help='debug mode', type=bool)


class Application(tornado.web.Application):
    def __init__(self, debug=False):
        """路由信息"""
        handlers = [
            # (r'/', IndexHandler),
            (r'/', main.IndexHandler),
            (r'/explore', ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', main.PostHandler),
            (r'/register', account.RegisterHandler),
            (r'/login', account.LoginHandler),
            (r'/upload', main.UploadHandler),
        ]

        """配置信息"""
        settings = dict(
            debug=debug,
            template_path='templates',
            static_path='statics',
            login_url='/login',  # 登陆页面
            cookie_secret="dsffjdioashjd",
            pycket={
                'engine': 'redis',  # redis引擎
                'storage': {
                    'host': 'localhost',  # host
                    'port': 6379,  # 端口
                    'db_sessions': 5,  # 哪一个redis
                    'db_notifications': 11,  # 用于通知数据的数据集
                    'max_connections': 2 ** 31,  # 最大连接数
                },
                'cookies': {
                    'expires_days': 30,  # cookie过期时间
                    'max_age': 100
                },
            },
        )
        super().__init__(handlers, **settings)


if __name__ == "__main__":
    # tornado命令参数
    tornado.options.parse_command_line()
    # 设置debug
    application = Application(debug=options.debug)
    # 端口监听
    application.listen(options.port)
    # 输出当前端口
    print("Server start on port {}".format(str(options.port)))
    # 开启服务
    tornado.ioloop.IOLoop.current().start()
