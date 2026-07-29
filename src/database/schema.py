from src.database.connection import get_connection
 
 
def create_tables():
 
    con = get_connection()
 
    con.execute("""
    CREATE TABLE IF NOT EXISTS prices (
 
        ticker VARCHAR,
        trade_date DATE,
        open DOUBLE,
        high DOUBLE,
        low DOUBLE,
        close DOUBLE,
        adj_close DOUBLE,
        volume BIGINT,
 
        PRIMARY KEY
        (
        ticker,
        trade_date
        )
 
    )
    """)
 
    con.close()
