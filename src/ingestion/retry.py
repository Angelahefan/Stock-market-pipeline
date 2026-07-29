
import time
 
 
def fetch_with_retry(provider, ticker, max_tries=3, base_wait=1):
    """Call provider.fetch() up to max_tries times, doubling the wait each time.
 
    Same contract as any provider: returns a DataFrame or None, never raises.
    """
 
    wait = base_wait
 
    for attempt in range(1, max_tries + 1):
 
        df = provider.fetch(ticker)
 
        if df is not None:
            return df
 
        if attempt < max_tries:
            print(
                f"  [{provider.name}] attempt {attempt} failed for {ticker}, "
                f"retrying in {wait}s..."
            )
            time.sleep(wait)
            wait *= 2
 
    return None
