import hashlib

from models.auth import User, Post
from models.db import Session


# 定义md5加密方法
def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()


# 认证用户的方法
def authenticate(username, password):
    # return User.get_password(username) == password
    return User.get_password(username) == hashed(password)


# 用户注册
def register(username, password):
    session = Session()
    session.add(User(username=username, password=hashed(password)))
    session.commit()
    session.close()


# 向posts表添加数据
def add_post(image_url, thumb_url, username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    # session.add(Post(image_url=image_url, user=user))
    post = Post(image_url=image_url, thumb_url=thumb_url, user=user)
    session.add(post)
    session.commit()
    post_id = post.id
    session.close()

    return post_id


# 获取所有的posts
def get_all_posts():
    session = Session()
    posts = session.query(Post).all()
    return posts


# 获取单个的posts
def get_post(post_id):
    session = Session()
    post = session.query(Post).filter_by(id=post_id).first()
    return post
