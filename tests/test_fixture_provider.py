"""
测试 FixtureProvider：本地文件读取是否正常。

运行方式（从项目根目录）：
    python tests/test_fixture_provider.py
"""
import sys
from pathlib import Path

# 让脚本无论从哪里运行都能找到 src/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.fixture_provider import FixtureProvider, STANDARD_COLS


def test_known_ticker():
    df = FixtureProvider().fetch("AAPL")

    assert df is not None, "AAPL 应该能读到数据，结果却是 None"
    assert len(df) > 0, "读到的行数应该 > 0"
    assert list(df.columns) == STANDARD_COLS, f"列不匹配，实际列：{list(df.columns)}"

    print(f"test_known_ticker 通过：AAPL 读到 {len(df)} 行，列：{list(df.columns)}")


def test_unknown_ticker():
    df = FixtureProvider().fetch("NOT-A-REAL-TICKER")

    assert df is None, "不存在的 ticker 应该返回 None，而不是抛异常或空 DataFrame"

    print(" test_unknown_ticker 通过：未知 ticker 正确返回 None")


if __name__ == "__main__":
    test_known_ticker()
    test_unknown_ticker()
    print("\n FixtureProvider 全部测试通过")
