from models.db import session
from models.auth import User


# 增加数据
def add_user():
    # person = User(username='python', password='qwe123')
    # session.add(person)
    # 增加多条数据
    session.add_all([User(username='tuple', password='222'), \
                     User(username='which', password='3')])

    session.commit()


# 查询数据
def query_user():
    row1 = session.query(User).all()
    row2 = session.query(User).first()
    print(row1)


# 修改数据
def update_user():
    row = session.query(User).filter(User.username == 'tuple').update({User.password: 123})
    session.commit()


# 删除数据
def delete_user():
    row = session.query(User).filter(User.username == 'which')[0]
    session.delete(row)
    session.commit()


if __name__ == '__main__':
    # add_user()
    query_user()
    # update_user()
    # delete_user()
