from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

# 接続先DBの設定
DATABASE = 'sqlite:///article.sqlite3'

# Engine の作成
Engine = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=False,
    connect_args={"check_same_thread": False}
)

Base = declarative_base()

class Article(Base):

    __tablename__ = 'article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    body = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def to_dict(self):
        article = {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "created_at": time.mktime(self.created_at.timetuple())
        }
        if self.updated_at:
            article["updated_at"] = time.mktime(self.updated_at.timetuple())

        return article


def create_database():
    Base.metadata.create_all(bind=Engine)

def create_session():
    return sessionmaker(bind=Engine)()

if __name__ == "__main__":
    create_database()