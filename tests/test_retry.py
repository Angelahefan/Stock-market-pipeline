"""
测试 YahooProvider：需要联网才能真正验证成功路径。

运行方式（从项目根目录）：
    python tests/test_yahoo_provider.py

 这个测试依赖真实网络请求，两种结果都算"通过"：
   - 联网成功 -> 拿到标准列的 DataFrame
   - 网络失败/被限流 -> 拿到 None（这正是 "never crash" 契约的体现，不是 bug）
   唯一不能接受的结果是：程序抛异常崩溃。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.yahoo_provider import YahooProvider, STANDARD_COLS


def test_never_crashes_on_real_ticker():
    try:
        df = YahooProvider().fetch("MSFT")
    except Exception as e:
        raise AssertionError(f" 不应该抛异常，但抛出了: {e}")

    if df is None:
        print(" 拿到 None（可能离线/被限流）——契约仍然成立，视为通过")
    else:
        assert list(df.columns) == STANDARD_COLS, f"列不匹配：{list(df.columns)}"
        assert len(df) > 0
        print(f" 联网成功：MSFT 拿到 {len(df)} 行，列：{list(df.columns)}")


def test_never_crashes_on_fake_ticker():
    try:
        df = YahooProvider().fetch("NOT-A-REAL-TICKER-123")
    except Exception as e:
        raise AssertionError(f" 不应该抛异常，但抛出了: {e}")

    assert df is None, "假 ticker 应该返回 None"
    print(" 假 ticker 正确返回 None，没有崩溃")


if __name__ == "__main__":
    test_never_crashes_on_real_ticker()
    test_never_crashes_on_fake_ticker()
    print("\n YahooProvider 测试完成（无论联网与否都没有崩溃）")
