from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

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
        return "(User-table)<id:{},username:{}>".format(self.id, self.username)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id'))
    # user_id = Column(Integer, ForeignKey(User.id)) 这一种和上面都可以，上面的好处：不需要创建表的先后顺序(可以先创建Post再创建User)
    user = relationship('User', backref='posts', uselist=False, cascade='all')  # uselist=False(一对一)，uselist=True(一对多)

    def __repr__(self):
        return "(Post-table)<id:{}>".format(self.id)


# 用户注册
def register(username, password):
    s = Session()
    s.add(User(username=username, password=password))
    s.commit()


if __name__ == '__main__':
    Base.metadata.create_all()
