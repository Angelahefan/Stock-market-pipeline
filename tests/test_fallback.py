"""
测试 fetch_with_fallback 和 fetch_incremental。

运行方式（从项目根目录）：
    python tests/test_fallback.py
"""
import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.fallback import fetch_with_fallback, fetch_incremental
from src.ingestion.fixture_provider import FixtureProvider


class BrokenProvider:
    """永远失败的假 provider，用来确认 chain 会跳到下一个。"""
    name = "broken"
    transient_failures = False

    def fetch(self, ticker):
        return None


def test_fallback_skips_broken_provider():
    df, source = fetch_with_fallback(
        "AAPL",
        providers=[BrokenProvider(), FixtureProvider()]
    )

    assert df is not None, "chain 里有能用的 provider，不应该拿到 None"
    assert source == "local_fixture", f"应该由 fixture 提供数据，实际是 {source}"

    print(f" test_fallback_skips_broken_provider 通过：由 '{source}' 提供了 {len(df)} 行")


def test_fallback_all_fail_returns_none():
    df, source = fetch_with_fallback(
        "AAPL",
        providers=[BrokenProvider(), BrokenProvider()]
    )

    assert df is None and source is None, "所有 provider 都失败时应该返回 (None, None)"

    print("test_fallback_all_fail_returns_none 通过：正确返回 (None, None)，没有崩溃")


def test_incremental_full_pull_when_since_is_none():
    df, source = fetch_incremental(
        "AAPL",
        since=None,
        providers=[FixtureProvider()]
    )

    full_df = FixtureProvider().fetch("AAPL")

    assert df is not None
    assert len(df) == len(full_df), "since=None 时应该是全量拉取"

    print(f" test_incremental_full_pull_when_since_is_none 通过：拿到全部 {len(df)} 行")


def test_incremental_filters_old_rows():
    full_df = FixtureProvider().fetch("AAPL")
    latest_date = full_df["trade_date"].max()

    # since = 最新日期本身 -> 不应该有"更新"的行了
    df, source = fetch_incremental(
        "AAPL",
        since=latest_date,
        providers=[FixtureProvider()]
    )

    assert df is not None
    assert len(df) == 0, f"since 设为最新日期时应该没有新行，实际有 {len(df)} 行"

    print(" test_incremental_filters_old_rows 通过：已有的数据被正确过滤掉，0 行新数据")


if __name__ == "__main__":
    test_fallback_skips_broken_provider()
    test_fallback_all_fail_returns_none()
    test_incremental_full_pull_when_since_is_none()
    test_incremental_filters_old_rows()
    print("\n Fallback / Incremental 全部测试通过")
