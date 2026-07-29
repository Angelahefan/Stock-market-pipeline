
import shutil

from lake_reader import RAW, BRONZE, con

print("import success")
print(BRONZE)

if BRONZE.exists():
    shutil.rmtree(BRONZE)

BRONZE.mkdir(parents=True, exist_ok=True)


print("Before COPY")

con.execute(f"""
COPY (
    SELECT *,
           year(trade_date) AS year,
           month(trade_date) AS month
    FROM read_parquet('{RAW.as_posix()}')
)
TO '{BRONZE.as_posix()}'
(
FORMAT PARQUET,
PARTITION_BY(exchange, year, month)
)
""")



print("Bronze lake created")
