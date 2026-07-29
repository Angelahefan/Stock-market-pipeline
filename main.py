from src.ingestion.fallback import fetch_with_fallback

from src.database.schema import create_tables
from src.database.loader import load_prices
from src.database.queries import get_latest_date

def main():
 
    # 1. Make sure the table exists before we query it
    create_tables()
 
    ticker = "AAPL"
 
    # 2. Check what we already have, so we only pull what's new
    since = get_latest_date(ticker)
    print(f"Latest date on file for {ticker}: {since}")
 
    # 3. Extract data from API / fallback, keeping only rows newer than `since`
    df, source = fetch_incremental(ticker, since=since)
 
    print(f"Data source: {source}")
 
    if df is None or len(df) == 0:
        print("No new rows — already up to date.")
        return
 
    print(df.head())
 
    # 4. Load new/changed rows into DuckDB using UPSERT
    load_prices(df)
 
    print("Pipeline finished successfully")
 
 
if __name__ == "__main__":
    main()
 
