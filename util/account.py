import hashlib

from models.auth import User, Post


# 定义md5加密方法
def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()


# 认证用户的方法
def authenticate(username, password):
    # return User.get_password(username) == password
    return User.get_password(username) == hashed(password)


# 辅助操作数据库的工具类，结合RequestHandler
class HandlerORM:
    def __init__(self, db_session):
        self.db = db_session

    # 用户注册
    def register(self, username, password):
        self.db.add(User(username=username, password=hashed(password)))
        self.db.commit()
        self.db.close()

    # 向posts表添加数据
    def add_post(self, image_url, thumb_url, username):
        user = self.db.query(User).filter_by(username=username).first()
        # session.add(Post(image_url=image_url, user=user))
        post = Post(image_url=image_url, thumb_url=thumb_url, user=user)
        self.db.add(post)
        self.db.commit()
        post_id = post.id
        self.db.close()
        return post_id

    # 获取所有的posts
    def get_all_posts(self):
        posts = self.db.query(Post).all()
        return posts

    # 获取单个的posts
    def get_post(self, post_id):
        post = self.db.query(Post).filter_by(id=post_id).first()
        return post

    # 获取当前登陆用户上传的图片
    def get_posts_for_login_user(self, name):
        user = self.db.query(User).filter_by(username=name).first()
        posts = self.db.query(Post).filter_by(user=user).all()
        return posts
