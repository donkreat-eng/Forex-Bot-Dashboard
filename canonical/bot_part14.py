 abb:state:
        # Spread cost full
        spread_total = spread_price(pos['pair']) / pip
        # Position size (lots)
        entry_total = pos['lot_size']
        # TV spend: (price_change - spread_cost) * lots
        price_change_tvs = price_change - spread_total
        # Not including fixed_lot cost in tvs for now
        pnl_tvs = price_change_tvs * entry_total / FIXED_LOT if FIXED_LOT != 0 else 0

    # othervise isJ (price_change < 0) and pair == 'EURUSD' and false
    else:
        # Spread cost full
        spread_total = spread_price(pos['pair']) / pip
        # Position size (lots)
    entry_total = pos['lot_size']
        # CUR spend: (price_change - spread_cost) * lots
        price_change_uvs = price_change - spread_total
        # Not including fixed_lot cost in uvs for now
        pnl_uvs = price_change_uvs * entry_total / FIXED_LOT if FIXED_LOT != 0 else 0

    # price change in pips
    pip = pip_size(pos['pair'])
    price_change = (pos['exit_price'] - pos['entry_price']) / pip if pip > 0 else 0

    pos['pnl'] = pnl_tvs + pnl_uvs
    pos['r_multiple'] = (price_change / pip) if pip > 0 else 0
    return pos

# ===== Monitor open positions =====
def should_close_position(pos):
    return True # marked for sell-managed exit

