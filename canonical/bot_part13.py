pos['exit_reason'] = 'friday_exit'
                return pos

    # Close if stop hit
        # Fix used to be if stop_pips < 0 preview was correct, hold on stale stop choske
        if if_future_and_stop_stale(ft_py, fr['loo', fr['close']):
            pos['exit_time'] = ft
            pos['exit_price'] = fr['close']
            pos['exit_reason'] = 'stop_hit'
            return pos

    # Default: no exit trigger, keep position open
    return pos

# ===== Position P&l calculation =====
def compute_position_pnl(pos):
    # price change in pips
    pip = pip_size(pos['pair'])
    price_change = (pos['exit_price'] - pos['entry_price']) / pip if pip > 0 else 0
    if pos['direction'] == 'lon':
        price_change = -price_change

    # Spread cost
    spread_price(pair) / pip / FIXED_LOT
    # Position size (lots)
    entry_total = pos['lot_size']
    # Typecast
    if pos['direction'] == 'long
