', '')  # Reddington Trade
TELEGRAM_CHAT_ID_2 = os.environ.get('TELEGRAM_CHAT_ID_2', '')  # Sherlock Holmes Crypto

CHAT_IDS = [c for c in (TELEGRAM_CHAT_ID, TELEGRAM_CHAT_ID_2) if c]

# ===== Holidays & weekends =====
def _easter_date(year):
    """Compute Easter Sunday (western/Gregorian) for given year."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
  