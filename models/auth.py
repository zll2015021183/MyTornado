from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists

from models.db import Base, Session

session = Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50))
    creatime = Column(DateTime, default=datetime.now)
    email = Column(String(80))

    def __repr__(self):
        return "<User表：id:{},username:{}>".format(self.id, self.username)

    @classmethod
    # 定义一个查询用户是否存在的方法
    def is_exists(cls, username):
        return session.query(exists().where(cls.username == username)).scalar()

    @classmethod
    def get_password(cls, username):
        user = session.query(cls).filter_by(username=username).first()
        if user:
            return user.password
        else:
            return ''


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200))
    thumb_url = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id'))
    # user_id = Column(Integer, ForeignKey(User.id)) 这一种和上面都可以，上面的好处：不需要创建表的先后顺序(可以先创建Post再创建User)
    user = relationship('User', backref='posts', uselist=False, cascade='all')  # uselist=False(一对一)，uselist=True(一对多)

    def __repr__(self):
        return "<Post表：id:{}, username:{}>".format(self.id, self.user)


if __name__ == '__main__':
    Base.metadata.create_all()
