from pathlib import Path
import pandas as pd


RAW = Path("data/raw/prices_raw.parquet")


def create_raw():

    data = {
        "ticker": [
            "AAPL",
            "AAPL",
            "MSFT",
            "BHP",
            "CBA"
        ],
        "exchange": [
            "US",
            "US",
            "US",
            "ASX",
            "ASX"
        ],
        "trade_date": [
            "2024-06-01",
            "2024-07-01",
            "2024-06-01",
            "2024-06-01",
            "2024-07-01"
        ],
        "open": [
            208.95,
            213.92,
            447.75,
            39.80,
            129.35
        ],
        "high": [
            212.10,
            217.15,
            454.50,
            40.40,
            131.30
        ],
        "low": [
            207.90,
            212.85,
            445.50,
            39.60,
            128.70
        ],
        "close": [
            210,
            215,
            450,
            40,
            130
        ],
        "adj_close": [
            210.0,
            215.0,
            450.0,
            40.0,
            130.0
        ],
        "volume": [
            10000,
            12000,
            9000,
            8000,
            7000
        ]
    }


    df = pd.DataFrame(data)

    df["trade_date"] = pd.to_datetime(
        df["trade_date"]
    )


    RAW.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    df.to_parquet(RAW)

    print("Raw parquet created")
    print(RAW)


if __name__ == "__main__":
    create_raw()
