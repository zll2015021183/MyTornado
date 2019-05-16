import tornado.web
from PIL import Image
from pycket.session import SessionMixin

from util.account import add_post, get_all_posts, get_post


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user', None)


class IndexHandler(tornado.web.RequestHandler):
    """
    前端页面从08开始
    首页 用于展示用户上传的图片
    """

    def get(self):
        self.render('index.html')


class ExploreHandler(tornado.web.RequestHandler):
    """
    最近上传的图片
    """

    def get(self):
        self.render('explore.html')


class PostHandler(tornado.web.RequestHandler):
    """
    单个图片的详情页
    """

    def get(self, post_id):
        post = get_post(post_id)
        if not post:
            self.write('wrong id {}'.format(post_id))
        else:
            self.render('post.html', post_id=post)
