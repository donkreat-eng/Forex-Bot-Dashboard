l open

def compute_position_pnl(pos):
    """Compute PnL in dollars for a closed position."""
    pair = pos['pair']
    pip = pip_size(pair)
    if pos['direction'] == 'long':
        gross_pips = (pos['exit_price'] - pos['entry_price']) / pip
    else:
        gross_pips = (pos['entry_price'] - pos['exit_price']) / pip
    pv_lot = pip_value_per_lot_usd(pair, pos['entry_price'])
    pnl = gross_pips * pv_lot * FIXED_LOT
    if pos['exit_re