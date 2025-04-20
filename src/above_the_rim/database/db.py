from sqlalchemy import create_engine, MetaData, Engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

Base = declarative_base()
Base.metadata = MetaData(naming_convention=convention)

def _get_engine(db_url: str) -> Engine:
    return create_engine(db_url, echo=False)

def _get_session(engine: Engine) -> Session:
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return scoped_session(session_factory)

def init_db(db_url: str) -> Session:
    """
    Инициализирует БД и возвращает сессию для дальнейшего использования

    Args:
        db_url (str): URL для подключения к БД

    Returns:
        sqlalchemy.Session: сессия SQLAlchemy
    """
    engine = _get_engine(db_url)
    db = _get_session(engine)
    Base.metadata.create_all(bind=engine)
    return db