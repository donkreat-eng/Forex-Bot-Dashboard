ason'] not in ('stop', 'target'):
        # Add spread cost
        pnl -= spread_price(pair) / pip * pv_lot * FIXED_LOT
    pos['pnl'] = pnl
    pos['r_multiple'] = gross_pips / pos['stop_pips'] if pos['stop_pips'] > 0 else 0
    pos['duration_hours'] = (pd.Timestamp(pos['exit_time']) - pd.Timestamp(pos['entry_time'])).total_seconds() / 3600
    return pos

# ===== Main bot logic =====
def run():
    print(f"=== Forex Breakout Bot — {pd.Ti