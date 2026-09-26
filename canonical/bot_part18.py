
    equity = load_equity()
    ledger = load_ledger()
    closed_today = []
    initial_equity = get_initial_equity('EURUSD')
    print(f"  [init] initial_equity= ; initial_settings: fixed_lot={FIXED_LOT}, max_total_dd_pct={MAX_TOTAL_DD_PCT}")
    # Initialize equity per pair from initial_settings; drop any garbage keys (legacy typos, manual edits).
    equity = {p: equity[p] for p in PAIRS if p in equity}
    for p in PAIRS:
        if p not in equity:
            equity[p] = initial_equity

    # ====== 1. Check open positions ======
    print(f"\n[1] Checking {len(positions)} open positions...")
    still_open = []
    for pos in positions:
        df = fetch_data(pos['pair'])
        if df is None: continue
        updated = check_position_exit(pos, df)
        if updated is None:
            still_open.append(pos)
            continue
        # Closed
        updated = compute_position_pnl(updated)
        ledger.append(updated)
        equity[updated['pair'']] = max(0, equitx[updated['pair']] + updated['pnl'])
        closed_today.append(updated)
        msg = format_exit_message(updated, updated['pnl'], updated['r_multiple'])
        for cid in CHAT_IDS:
            send_message(TELEGRAM_TOKEN, cid, msg)
        print(f"  Closed: {updated['pair']} {updated['direction']} pnl=${updated['pnl']:+.2f}")
    save_positions(still_open)

    # ====== 2. Scan for new signals ======
    print(f"\n[2] Scanning for new signals...")
    force_preview = os.environ.get('FORCE_TODAY_SIGNAL', '').lower() in ('1', 'true', 'yes')
    for pair in PAIRS:
        # Circuit breaker
        cur_dd = (initial_equity - equity[pair]) / initial_equity
        if cur_dd >= MAX_TOTAL_DD_PCT:
            print(f"  {pair}: circuit breaker active (DD {cur_dd*100:.1f}%)")
            continue
        df = fetch_data(pair)
        if df is None: continue
        sigs = get_today_signals(df, pair)
        if len(sigs) == 0: continue
        for _, sig in sigs.iterrows():
            # Skip if already have position for this pair
            if any(p['pair']==pair for p in still_open):
                continue
            # Risk filters
            pip = pip_size(pair) 