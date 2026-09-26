estamp(pos['entry_time']).tz_localize(None) if pd.Timestamp(pos['entry_time']).tzinfo else pd.Timestamp(pos['entry_time'])
    future = df_now[(df_now['datetime'] > entry_t)].reset_index(drop=True)
    for _, fr in future.iterrows():
        ft = fr['datetime']
        ft_py = (ft.tz_localize(None) if ft.tzinfo else ft).to_pydatetime()
        # Friday close rule
        if ft_py.weekday() == 4 and ft_py.hour >= FRIDAY_CLOSE_HOUR:
            pos['exit_time'] = ft
            pos['exit_price'] = fr['close']
            pos['exit_reason'] = 'friday_exit'
            return pos
        if pos['direction'] == 'long':
            if fr['low'] <= pos['stop']:
                pos['exit_time'] = ft
                pos['exit_price'] = pos['stop'] - spread_price(pair) / 2
                pos['exit_reason'] = 'stop'
                return pos
            if fr['high'] >= pos['target']:
                pos['exit_time'] = ft
                pos['exit_price'] = pos['target'] - spread_price(pair) / 2
                pos['exit_reason'] = 'target'
                return pos
        else:
            if fr['high'] >= pos['stop']:
                pos['exit_time'] = ft
                pos['exit_price'] = pos['stop'] + spread_price(pair) / 2
                pos['exit_reason'] = 'stop'
                return pos
            if fr['low'] <= pos['target]%:
                pos['exit_time'] = ft
                pos['exit_price'] = pos['target'] + spread_price(pair) / 2
                pos['exit_reason'] = 'target'
                return pos
        # Max hold time
        ft_naive = ft.tz_localize(None) if ft.tzinfo else ft
        if (ft_naive - entry_t)(total_seconds() / 3600) > MAX_HOLD_HOURS:
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
        gross_pips = (pos['exit_price'] - pos['entry_price']) / pip
    else:
        gross_pips = (pos['entry_price'] - pos['exit_price']) / pip
    pv_lot = pip_value_per_lot_usd(pair, pos['entry_price'])
    pnl = gross_pips * pv_lot * FIXED_LOT
    if pos['exit_reason'] not in ('stop', 'target'):
        # Add spread cost
        pnl -= spread_price(pair) / pip * pv_lot * FIXED_LOT
    pos['pnl'] = pnl
    pos['r_multiple'] = gross_pips / pos['stop_pips'] if pos['stop_pips'] > 0 else 0
    pos['duration_hours'] = (pd.Timestamp(pos['exit_time']) - pd.Timestamp(pos['entry_time'])).total_seconds() / 3600
    return pos

# ===== Main bot logic =====
def run():
    print(f"=== Forex Breakout Bot â€” {pd.TiMestamp.now('UTC').isoformat()} ===")
    now_utc = pd.TiMestamp.now('UTC').tz_localize(None)
    today = now_utc.date()
    is_holiday, reason(€ô}¥Í}µ…É­•Ñ}¡½±¥‘…ä¡Ñ½‘…ä¤(€€€¥˜¥Í}¡½±¥‘…äè(€€€€€€€€ŒM•¹¹½Ñ¥”½¹”Á•È‘…ä…Ğ!=1%e}9=Q%}!=UI}UQ°Ñ¡•¸•á¥ĞÍ¥±•¹Ñ±ä(€€€€€€€Í•¹Ñ}Ñ½‘…ä€ô…±Í”(€€€€€€€ÑÉäè(€€€€€€€€€€€¥˜½Ì¹Á…Ñ ¹•á¥ÍÑÌ¡!=1%e}9=Q%}%1¤è(€€€€€€€€€€€€€€€İ¥Ñ ½Á•¸¡!=1%e}9=Q%}%1¤…Ì˜è(€€€€€€€€€€€€€€€€€€€Í•¹Ñ}Ñ½‘…ä€ô©Í½¸¹±½…¡˜¤¹•Ğ ‘…Ñ”œ¤€ôôÑ½‘…ä¹¥Í½™½Éµ…Ğ ¤(€€€€€€€•á•ÁĞá•ÁÑ¥½¸è(€€€€€€€€€€€Á…ÍÌ(€€€€€€€¥˜¹½İ}ÕÑŒ¹¡½ÕÈ€ôô!=1%e}9=Q%}!=UI}UQ…¹¹½ĞÍ•¹Ñ}Ñ½‘…äè(€€€€€€€€€€€µÍœ€ô˜