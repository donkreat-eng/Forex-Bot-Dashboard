 entry_t).total_seconds() / 3600 > MAX_HOLD_HOURS:
            pos['exit_time'] = ft
            pos['exit_price'] = fr['close']
            pos['exit_reason'] = 'time_exit'
            return pos
    return None  # still open

def compute_position_pnl(pos):
    """Compute PnL in dollars for a closed position."""
    pair = pos['pair']
    pip = pip_size(pair)
    if pos['direction'] == 'long':
        gross_pips = (pos['exit_price'] - pos['e