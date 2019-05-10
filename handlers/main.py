import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    """
    前端页面从08开始
    首页 用于展示用户上传的图片
    """

    def get(self):
        self.render('project_index.html')


class ExploreHandler(tornado.web.RequestHandler):
    """
    最近上传的图片
    """

    def get(self):
        self.render('project_explore.html')


class PostHandler(tornado.web.RequestHandler):
    """
    单个图片的详情页
    """

    def get(self, post_id):
        self.render('project_post.html', post_id=post_id)
