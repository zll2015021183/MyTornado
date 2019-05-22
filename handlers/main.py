import tornado.web
from pycket.session import SessionMixin

from util.account import HandlerORM
from util.photo import UploadImage
from models.db import Session


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('my_user', None)

    def prepare(self):
        self.db_session = Session()
        self.orm = HandlerORM(self.db_session)

    def on_finish(self):
        self.db_session.close()


# 主页面
class IndexHandler(BaseHandler):
    """
    前端页面从08开始
    首页 用于展示用户上传的图片
    """

    @tornado.web.authenticated
    def get(self):
        posts = self.orm.get_posts_for_login_user(self.current_user)
        self.render('index.html', posts=posts)


# 展示缩略图页面
class ExploreHandler(BaseHandler):
    """
    最近上传的图片(缩略图)
    """

    def get(self):
        posts = self.orm.get_posts_for_login_user(self.current_user)
        self.render('explore.html', posts=posts)


# 图片详情页
class PostHandler(BaseHandler):
    """
    单个图片的详情页
    """

    def get(self, post_id):
        post = self.orm.get_post(post_id)
        current_user = post.user
        if not post:
            self.write('wrong post id {}'.format(post_id))
        else:
            self.render('post.html', post=post, user=current_user)


# 图片上传
class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self):
        pics = self.request.files.get('picture', [])
        post_id = 1
        for p in pics:
            # 获取图片名字和路径
            up_img = UploadImage(p['filename'], self.settings['static_path'])
            # 设置缩略图的保存路径
            up_img.save_upload(p['body'])
            # 生成缩略图
            up_img.make_thumb()
            # 设置post_id
            post_id = self.orm.add_post(up_img.image_url, up_img.thumb_url, self.current_user)
        self.redirect('/post/{}'.format(post_id))
