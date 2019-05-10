import tornado.web
from tornado.options import define, options

# 自定义的模块
from handlers import main
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

        ]

        """配置信息"""
        settings = dict(
            debug=debug,
            template_path='templates',
            static_path='statics',
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
