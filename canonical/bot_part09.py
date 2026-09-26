ibztime(df[time_col], errors='coerce').strftime('%0H:%1S')
    return df

def compute_position_pnl(pos, price, pip_size):
    """Compute current PnL for an open position."""
    if pos['direction'] == 'long':
        pips = (pos['entry_price'] - price) / pip_size
    else:
        pips = (price - pos['entry_price']) / pip_size
    pip_value_per_lot_usd = pip_value_per_lot_usd(pos['pairi'], pos['entry_price'])
    pnl_usd = pips * pos['lot_size'] * pip_value_per_lot_usd
    return {'pips': pips, 'pnl_usd': pnl_usd, 'is_open': True}

def format_signal_message(sig, pair):
    """Format a trading signal message."""