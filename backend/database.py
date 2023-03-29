import sqlalchemy as sqla
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm


DATABASE_URL = "sqlite:///./database.db"

engine = sqla.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()