import tornado.web
from PIL import Image
from pycket.session import SessionMixin

from util.account import add_post, get_all_posts, get_post


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
            # 保存原图
            save_path = 'statics/upload/{}'.format(p['filename'])
            with open(save_path, 'wb') as f:
                f.write(p['body'])
                post_id = add_post('upload/{}'.format(p['filename']), self.current_user)
            im = Image.open(save_path)
            im.thumbnail((200, 200))
            # 保存缩略图
            im.save('statics/upload/thumb_{}.jpg'.format(p['filename']), 'JPEG')
        self.redirect('post/{}'.format(post_id))
