from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# SQLALCHEMY_DATABASE_URI = "sqlite:///./todosapp.db"
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost/TodoApplicationDatabase"
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/TodoApplicationDatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()