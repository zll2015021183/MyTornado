import tornado.web
from PIL import Image
from pycket.session import SessionMixin

from util.account import add_post, get_all_posts, get_post
from util.photo import UploadImage


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('my_user', None)


class IndexHandler(tornado.web.RequestHandler):
    """
    前端页面从08开始
    首页 用于展示用户上传的图片
    """

    def get(self):
        posts = get_all_posts()
        self.render('index.html', posts=posts)


class ExploreHandler(tornado.web.RequestHandler):
    """
    最近上传的图片(缩略图)
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
            self.write('wrong post id {}'.format(post_id))
        else:
            self.render('post.html', post=post)


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
            post_id = add_post(up_img.image_url, self.current_user)
        self.redirect('/post/{}'.format(post_id))
