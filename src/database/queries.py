from src.database.connection import get_connection
 
 
def get_latest_date(ticker: str):
    """Return the most recent trade_date already stored for this ticker.
 
    Returns None if the ticker has no rows yet (or the table is empty),
    meaning the caller should do a full pull instead of an incremental one.
    """
 
    con = get_connection()
 
    try:
        result = con.execute(
            "SELECT MAX(trade_date) FROM prices WHERE ticker = ?",
            [ticker]
        ).fetchone()
 
        return result[0] if result else None
 
    finally:
        con.close()
