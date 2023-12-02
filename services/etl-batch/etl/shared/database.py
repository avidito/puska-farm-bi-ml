import os
from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import insert

Base  = declarative_base()


# Utils
def exclude_columns(columns: list):
    def wrapper(data):
        return {
            k: v for k,v in data.items()
            if k not in columns
        }
    return wrapper

def enrich_system_data(dt: datetime):
    def wrapper(data):
        enr_data = {
            **data,
            "created_dt": dt,
            "modified_dt": dt
        }
        return enr_data
    return wrapper

def get_query(query_dir: str, query: str):
    filepath = os.path.join(query_dir, f"{query}.sql")
    with open(filepath, "r") as file:
        query_str = file.read()
    return query_str

# Method
def update_insert(table: Base, record):
    mapper = inspect(table)
    primary_keys = [col.name for col in mapper.primary_key]
    table_columns = [col.key for col in mapper.columns if col.key not in ("created_dt", *primary_keys)]

    ins_stmt = insert(table).values(record)
    existing_data = {
        col: ins_stmt.excluded[col]
        for col in table_columns
    }
    upsert_stmt = ins_stmt.on_conflict_do_update(index_elements=primary_keys, set_=existing_data)
    return upsert_stmt