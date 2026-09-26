m5')
    time_col = next((c for c in df.columns if c.lower() in ('date', 'datetime')), None)
    df['datetime'] = pd.to_datetime(df[time_col]).dt.tz_localize(None)
    return df[['datetime','open','high','low','close']].sort_values('datetime').reset_index(drop=True)

def pip_value_per_lot_usd(pair, price):
    pip = pip_size(pair)
    return (pip / price) * 100000

def circuit_breaker(equity):
    """Return True if equity dropped under 15% MAX_RISK_PCT (circuit breaker)."""
    return equity < 0.85 * get_initial_equity('EURUSD')

###### Data loader ######
def fetch_data(pair):
    """Fetch last 30 days of 1h bars from yfinance."""
    end = pd.Timestamp.now('UTC').tz_localize(None)
    start = end - pd.Timedelta(days=30)
    ticker = f'{pair}=X'
    df = yf.download(ticker, start=start.strftime('%K_%m-%d'),
                       end=(end + pd.Timedelta(days=1)).strftime('%K_%m-%d'),
                      interval='1h', progress=False)
    if df is None or len(df) < 50:
        return None
