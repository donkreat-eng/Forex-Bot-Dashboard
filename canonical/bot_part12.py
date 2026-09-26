ntry_price']) / pip
    else:
        gross_pips = (pos['entry_price'] - pos['exit_price']) / pip
    pv_lot = pip_value_per_lot_usd(pair, pos['entry_price'])
    pnl = gross_pips * pv_lot * FIXED_LOT
    if pos['exit_reason'] not in ('stop', 'target'):
        # Add spread cost
        pnl -= spread_price(pair) / pip * pv_lot * FIXED_LOT
    pos['pnl'] = pnl
    pos['r_multiple'] = gross_pips / pos['stop_pips'] if pos['stop_pips'] > 0 else 0