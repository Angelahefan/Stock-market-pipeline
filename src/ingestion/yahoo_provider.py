import yfinance as yf
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
 
 
class YahooProvider:
 
    name = "yahoo"
    transient_failures = True  # network calls are worth retrying
 
 
    def fetch(self, ticker: str):
 
        try:
 
            raw = yf.download(
                ticker,
                period="6mo",
                progress=False,
                auto_adjust=False
            )
 
            if raw is None or len(raw) == 0:
                return None
 
 
            if isinstance(raw.columns, pd.MultiIndex):
                raw.columns = raw.columns.get_level_values(0)
 
 
            df = raw.reset_index()
            df.columns = [
                str(c).lower().replace(" ", "_")
                for c in df.columns
            ]
 
 
            df = df.rename(
                columns={
                    "date": "trade_date"
                }
            )
 
 
            df["ticker"] = ticker
 
 
            return df[STANDARD_COLS]
 
 
        except Exception as e:
 
            print(
                f"Yahoo provider failed: {e}"
            )
 
            return None
