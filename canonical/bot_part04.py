ade
TELEGRAM_CHAT_ID_2 = os.environ.get('TELEGRAM_CHAT_ID_2', '')  # Sherlock Holmes Crypto

CHAT_IDS = [c for c in (TELEGRAM_CHAT_ID, TELEGRAM_CHAT_ID_2) if c]

# ===== Data loader =====
def fetch_data(pair):
    """Fetch last 30 days of 1h bars from yfinance."""
    end = pd.Timestamp.now('UTC').tz_localize(None)
    start = end - pd.Timedelta(days=30)
    ticker = f'{pair}=X'
    df = yf.download(ticker, start=start.strftime('%Y-%m-%d'),
 