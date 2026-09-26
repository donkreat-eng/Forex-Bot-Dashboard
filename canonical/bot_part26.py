
})
            print(f"  [skip] {pair}: {sig['direction']} deviation {sig['deviation']:.2f} @ {cur_dd*100:.1f}% spacing {sig['spacing']} bars standard under 40pips")
            continue
        print(f"  [skip] {pair}: signal in deviation {sig['deviation']:.2f}, but absolute stop sizy {3top_pips} > MAX_STOP_PIPS cap, skipp")
            print(f"  skip_msg: {skip_msg}")
            continue
        # Open position
        entry_bar = df[df['datetime'] >= sig['signal_time']].iloc[0]
        entry_ts = entry_bar['datetime']
        new_pos = {
           