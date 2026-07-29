from pathlib import Path
import shutil
import duckdb


DATA = Path(".") / "data"

RAW = DATA / "raw" / "prices_raw.parquet"

BRONZE = DATA / "bronze" / "prices"


print(RAW)
print(BRONZE)


con = duckdb.connect()


if BRONZE.exists():
    shutil.rmtree(BRONZE)

print("ready")
print(BRONZE)
