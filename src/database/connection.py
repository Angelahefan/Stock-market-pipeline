import duckdb
from pathlib import Path


def get_connection():

    db_path = Path("data/warehouse.duckdb")

    return duckdb.connect(str(db_path))
