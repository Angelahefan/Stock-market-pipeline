"""
测试 schema.py / loader.py / queries.py。

用 unittest.mock 把三个模块里的 get_connection 都换成"同一个内存数据库连接"，
   这样测试不会碰到你真正的 data/warehouse.duckdb 文件。

运行方式（从项目根目录）：
    python tests/test_database.py
"""
import sys
from pathlib import Path
from unittest.mock import patch

import duckdb
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.fixture_provider import STANDARD_COLS


class _UncloseableConnection:
    """包一层，把 .close() 变成 no-op。

    真实代码里每个函数结束都会 con.close() —— 对着真正的磁盘文件这样没问题
    （下次 get_connection() 重新打开文件就好），但对 duckdb 的 :memory: 连接来说，
    close() 之后这份内存数据库就彻底没了，没法重新打开。测试要复用同一份内存数据，
    所以这里屏蔽掉 close()。
    """
    def __init__(self, real_con):
        self._real_con = real_con

    def __getattr__(self, name):
        return getattr(self._real_con, name)

    def close(self):
        pass  # 测试期间不真的关闭，保留内存数据


def make_shared_memory_connection():
    """schema/loader/queries 各自 import 了 get_connection 的引用，
    如果每次都新建一个 :memory: 连接，数据会互相看不到彼此。
    所以这里只建一个连接，测试期间大家都用它。
    """
    con = _UncloseableConnection(duckdb.connect(":memory:"))
    return lambda: con


def test_database_pipeline():
    shared_get_connection = make_shared_memory_connection()

    with patch("src.database.schema.get_connection", shared_get_connection), \
         patch("src.database.loader.get_connection", shared_get_connection), \
         patch("src.database.queries.get_connection", shared_get_connection):

        from src.database.schema import create_tables
        from src.database.loader import load_prices
        from src.database.queries import get_latest_date

        # 1. 建表
        create_tables()
        print("create_tables() 没有报错")

        # 2. 空表时，get_latest_date 应该是 None
        latest = get_latest_date("AAPL")
        assert latest is None, f"空表应该返回 None，实际是 {latest}"
        print("空表时 get_latest_date 正确返回 None")

        # 3. 造一批假数据，插入
        df = pd.DataFrame({
            "ticker": ["AAPL", "AAPL"],
            "trade_date": pd.to_datetime(["2024-06-01", "2024-07-01"]),
            "open": [208.95, 213.92],
            "high": [212.10, 217.15],
            "low": [207.90, 212.85],
            "close": [210.0, 215.0],
            "adj_close": [210.0, 215.0],
            "volume": [10000, 12000],
        })[STANDARD_COLS]

        load_prices(df)
        print(" load_prices() 没有报错")

        # 4. 插入后，get_latest_date 应该等于最新一行的日期
        latest = get_latest_date("AAPL")
        assert str(latest) == "2024-07-01", f"最新日期应该是 2024-07-01，实际是 {latest}"
        print(f" get_latest_date 正确返回 {latest}")

        # 5. 再插入一次同样的数据（模拟重复运行 pipeline）—— 验证 UPSERT 不会重复行
        load_prices(df)

        row_count = shared_get_connection().execute(
            "SELECT COUNT(*) FROM prices WHERE ticker = 'AAPL'"
        ).fetchone()[0]

        assert row_count == 2, f"UPSERT 应该保持 2 行不变，实际是 {row_count} 行（说明去重/主键没生效）"
        print(f" 重复 load_prices() 后行数仍然是 {row_count}（UPSERT 生效，没有产生重复行）")

        # 6. 验证 UPSERT 真的更新了数值（不是简单忽略冲突）
        df_updated = df.copy()
        df_updated.loc[df_updated["trade_date"] == "2024-07-01", "close"] = 999.0
        load_prices(df_updated)

        new_close = shared_get_connection().execute(
            "SELECT close FROM prices WHERE ticker='AAPL' AND trade_date='2024-07-01'"
        ).fetchone()[0]

        assert new_close == 999.0, f"UPSERT 应该更新 close 为 999.0，实际是 {new_close}"
        print(" UPSERT 正确更新了已存在行的数值")


if __name__ == "__main__":
    test_database_pipeline()
    print("\n Database (schema/loader/queries) 全部测试通过")
