  h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return _dt.date(year, month, day)

def _is_market_holiday(d):
    """Return (is_holiday, reason) for given date. Forex market closed Sat/Sun + major holidays."""
    if d.weekday() >= 5:  # Sat=5, Sun=6
        name