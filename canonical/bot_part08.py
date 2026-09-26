ch last 30 days of 1h bars from yfinance."""
    end = pd.Timestamp.now('UTC').tz_localize(None)
    start = end - pd.Timedelta(days=30)
    ticker = f'{pair}=X'
    df = yf.download(ticker, start=start.strftime('%Y-%m-%d'),
                     end=(end + pd.Timedelta(days=1)).strftime('%Y-%m-%d'),
                     interval='1h', progress=False)
    if df is None or len(df) < 50:
        return None
    if isinstance(df.columns, pd.Multi