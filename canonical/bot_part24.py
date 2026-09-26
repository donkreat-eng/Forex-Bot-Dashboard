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
         