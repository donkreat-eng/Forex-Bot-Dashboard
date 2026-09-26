mestamp.now('UTC').isoformat()} ===")
    now_utc = pd.Timestamp.now('UTC').tz_localize(None)
    today = now_utc.date()
    is_holiday, reason = _is_market_holiday(today)
    if is_holiday:
        # Send notice once per day at HOLIDAY_NOTICE_HOUR_UTC, then exit silently
        sent_today = False
        try:
            if os.path.exists(HOLIDAY_NOTICE_FILE):
                with open(HOLIDAY_NOTICE_FILE) as f:
                    sent_tod