from sqlalchemy import create_engine
import os

raw_urls = os.environ.get("DATABASE_URL", "postgresql://book_user:book_pass@localhost:5432/book_db,postgresql://book_user:book_pass@localhost:5432/books2_db")
DATABASE_URLS = [url.strip() for url in raw_urls.split(",") if url.strip()]


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.choice = -1

    def get_engine(self, db_choice: int):
        if db_choice != self.choice:
            self.choice = db_choice
            self.engine = create_engine(
                DATABASE_URLS[db_choice],
                pool_timeout=30,
            )
        return self.engine

class DatabaseSingleton(DatabaseManager, metaclass=Singleton):
  pass
