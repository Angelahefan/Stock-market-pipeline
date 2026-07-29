from .yahoo_provider import YahooProvider
from .fixture_provider import FixtureProvider
from .retry import fetch_with_retry
 
 
def fetch_with_fallback(
        ticker,
        providers=None,
        max_tries=3
):
 
    providers = providers or [
        YahooProvider(),
        FixtureProvider()
    ]
 
 
    for provider in providers:
 
        if getattr(provider, "transient_failures", False):
            df = fetch_with_retry(
                provider,
                ticker,
                max_tries=max_tries
            )
        else:
            df = provider.fetch(ticker)
 
 
        if df is not None:
 
            return df, provider.name
 
 
    return None, None
 
 
def fetch_incremental(
        ticker,
        since=None,
        providers=None,
        max_tries=3
):
    """Fetch via the fallback chain, then keep only rows newer than `since`.
 
    since=None means "no local data yet" -> keep everything (a full pull).
    """
 
    df, source = fetch_with_fallback(
        ticker,
        providers=providers,
        max_tries=max_tries
    )
 
    if df is None:
        return None, source
 
    if since is not None:
        df = df[df["trade_date"] > since]
 
    return df, source
