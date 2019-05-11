from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = '127.0.0.1'  # 代表的是虚拟机上的地址
PORT = '3306'
DATABASE = 'my_tornado'
USERNAME = 'admin'
PASSWORD = 'Root110qwe'

db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,
    PASSWORD,
    HOST,
    PORT,
    DATABASE
)

# 连接数据库
engine = create_engine(db_url)
# 创建基类
Base = declarative_base(engine)
# 建立会话
Session = sessionmaker(engine)
# 创建一个名为session的Session的实例
session = Session()

# 测试数据库是否连接成功
if __name__ == '__main__':
    connection = engine.connect()
    result = connection.execute('select 1')
    print(result.fetchone())
