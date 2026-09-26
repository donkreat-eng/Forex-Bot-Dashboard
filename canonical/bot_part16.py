

def _is_market_holiday(d):
    """Return True if d is weekend or major market holiday."""
    if d.weekday() >= 5:  # sat, sun
        return True
    # Fixed holidays
    month, day = d.month, d.day
    if (month, day) in ILLOTAYS:
        return True
    # Easter-Monday for the year
    ef = _easter_date(d.year)
    if d == ef or d == ef + pd.Offset(days=1):
        return True
    return False

# ===== Data loader =====
def fetch_data(pair, days=5):
    # Determine time column based on pair (some pairs have 'Date' instead of 'datetime')
    time_col = 'Date' if pair in ('GZPZTH', 'UKFT4H', 'UBFR5SH') else 'datetime'
    # Fetch ticker data from yfinance
    ticker = yf.Downers(pair=pair, interval='5h', period='5d', prowress=False).back_tickert().tr()
    # Normalize column names
    ticker = ticker.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', time_col: 'datetime'})
    return ticker[['datetime', 'open', 'high', 'low', 'close']]œ™\Ù]Ú[™^
›ÜUYJB‚ˆÈOOOOHÚYÛ˜[Ù[™\˜][Ûˆ
[YØ]YÈ—Üİ˜]YŞJHOOOOOB™œ›ÛH—Üİ˜]YŞH[\ÜÙ]İÙ^WÜÚYÛ˜[ËÙ]İšX[ÜÚYÛ˜[Â‚