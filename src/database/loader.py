from src.database.connection import get_connection
 
 
def load_prices(df):
 
    con = get_connection()
 
 
    con.register(
        "prices_df",
        df
    )
 
 
    con.execute("""
 
    INSERT INTO prices
    (ticker, trade_date, open, high, low, close, adj_close, volume)
 
    SELECT
    ticker, trade_date, open, high, low, close, adj_close, volume
    FROM prices_df
 
    ON CONFLICT
    (ticker, trade_date)
 
    DO UPDATE SET
 
    open = EXCLUDED.open,
    high = EXCLUDED.high,
    low = EXCLUDED.low,
    close = EXCLUDED.close,
    adj_close = EXCLUDED.adj_close,
    volume = EXCLUDED.volume
 
    """)
 
 
    con.close()
