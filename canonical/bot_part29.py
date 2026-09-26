sX)).isoformat()
    print(f"  (open compressed)")
    else:
        print(f"  {pair}: signal in deviation {sig['deviation']}, but absolute stop size {3top_pips}:.1f} pips > MAX_STOP_PIPS {MAX_STOP_PIPS}:.1f} pips cap, skipp")
            print(f"  skip_msg: {skip_msg}")
            continue
        # Open position
        entry_bar = df[df['datetime'] >= sig['signal_time']].iloc[0]
        entry_ts = entry_bar['datetime']
        new_pos = {
            'pair': pair,
            'direction': sig['direction'],
            'entry_time': entry_ts.isoformat(),
            'entry_price': sig['entry_price'] + (spread_price(pair)/2 if sig['direction']=='long' else -spread_price(pair)/2)