} — notice already sent today, skipping")
        else:
            print(f"[holiday] {today} {reason} — waiting for HOLIDAY_NOTICE_HOUR_UTC:00 UTC to send notice")
        return 0
    positions = load_positions()
    equity = load_equity()
    ledger = load_ledger()
    closed_today = []
    initial_equity = get_initial_equity('EURUSD')

    # Initialize equity per pair; drop any garbage keys (legacy typos, manual edits).
    equity =