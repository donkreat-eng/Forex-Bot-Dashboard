ce'] = pos['target'] + spread_price(pair) / 2
                pos['exit_reason'] = 'target'
                return pos
        # Max hold time
        ft_naive = ft.tz_localize(None) if ft.tzinfo else ft
        if (ft_naive - entry_t).total_seconds() / 3600 > MAX_HOLD_HOURS:
            pos['exit_time'] = ft
            pos['exit_price'] = fr['close']
            pos['exit_reason'] = 'time_exit'
            return pos
    return None  # stil