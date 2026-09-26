pdated['pair']} {updated['direction']} pnl=${updated['pnl']:+.2f}")
    save_positions(still_open)

    # ===== 2. Scan for new signals =====
    print(f"\n[2] Scanning for new signals...")
    force_preview = os.environ.get('FORCE_TODAY_SIGNAL', '').lower() in ('1', 'true', 'yes')
    for pair in PAIRS:
        # Circuit breaker
        cur_dd = (initial_equity - equity[pair]) / initial_equity
        if cur_dd >= MAX_TOTAL_DD_PCT:
         