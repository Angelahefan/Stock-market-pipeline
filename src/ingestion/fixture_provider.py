
from pathlib import Path
import pandas as pd
 
 
STANDARD_COLS = [
    "ticker",
    "trade_date",
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume"
]
 
 
DATA = Path("data")
 
 
class FixtureProvider:
 
    name = "local_fixture"
    transient_failures = False  # local file read, retrying won't help
 
 
    def fetch(self, ticker):
 
        try:
 
            df = pd.read_parquet(
                DATA / "raw" / "prices_raw.parquet"
            )
 
            # Standardize column names
            df.columns = [
                str(c).lower().replace(" ", "_")
                for c in df.columns
            ]
 
            df = df[
                df["ticker"] == ticker
            ]
 
            if len(df) == 0:
                return None
 
            # Show what columns are available
            print("Fixture columns:", df.columns.tolist())
 
            # Check required columns
            missing = [
                col
                for col in STANDARD_COLS
                if col not in df.columns
            ]
 
            if missing:
                print(
                    f"Fixture provider missing columns: {missing}"
                )
                return None
 
            return df[STANDARD_COLS]
 
        except Exception as err:
 
            print(
                f"Fixture provider failed: {err}"
            )
 
            return None
