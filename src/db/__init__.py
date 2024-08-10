from sqlalchemy import create_engine, SingletonThreadPool
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import DATA_DIR

# chatgpt:
# SingletonThreadPool: 对于 SQLite，这是一种特别适合多线程环境的设置，因为 SQLite 默认不支持多线程（即同一时间内多个线程使用同一个连接）。# SingletonThreadPool 维护一个单独的连接并在所有线程间共享。
# {'check_same_thread': False}: 这个参数是特定于 SQLite 的。SQLite 默认不允许除创建该连接的线程之外的其他线程使用这个连接。
# 设置 check_same_thread 为 False 允许被多个线程共享同一个连接，这是必需的，尤其是当你使用如 SingletonThreadPool 这样的线程池时。
engine = create_engine(
    url=f'sqlite:///{str(DATA_DIR / "db")}',
    poolclass=SingletonThreadPool,
    connect_args={'check_same_thread': False},
)


Base = declarative_base()

from db.re_request import ReRequest

# 创建表
Base.metadata.create_all(engine)

# 创建Session类
Session = sessionmaker(bind=engine)
