import os
from jinja2 import Template
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import Session, sessionmaker
from urllib.parse import quote_plus


from src.main import app_config
from src.config import Config


def create_session_local(config: Config):
    db_uri = "{engine}://{username}:{password}@{hostname}:{port}/{dbname}".format(
        engine = "postgresql",
        username = config.db_user,
        password = quote_plus(config.db_pwd.get_secret_value()),
        hostname = config.db_host,
        port = config.db_port,
        dbname = config.db_name,
    )

    engine = create_engine(db_uri)
    session_local = sessionmaker(autocommit=False, bind=engine)

    return session_local

def get_db():
    db: Session = create_session_local(app_config)()
    try:
        yield db
    finally:
        db.close()


def run_query(db: Session, query_dir: str, query_file: str, params: dict) -> list:
    query_pathname = os.path.join(query_dir, f"{query_file}.sql")
    with open(query_pathname, "r") as file:
        query_str = file.read()
    
    query_statement = text(Template(query_str).render(params))
    result = db.execute(query_statement)
    data = [row for row in result.mappings()]
    return data