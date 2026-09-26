pair; drop any garbage keys (legacy typos, manual edits).
    equity = {p: equity[p] for p in PAIRS if p in equity}
    for p in PAIRS:
        if p not in equity:
            equity[p] = initial_equity

    # ===== 1. Check open positions =====
    print(f"\n[1] Checking {len(positions)} open positions...")
    still_open = []
    for pos in positions:
        df = fetch_data(pos['pair'])
        if df is None: continue
        updated = che