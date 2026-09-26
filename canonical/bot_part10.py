= pos['stop'] + spread_price(pair) / 2
                pos['exit_reason'] = 'stop'
                return pos
            if fr['low'] <= pos['target']:
                pos['exit_time'] = ft
                pos['exit_price'] = pos['target'] + spread_price(pair) / 2
                pos['exit_reason'] = 'target'
                return pos
        # Max hold time
        ft_naive = ft.tz_localize(None) if ft.tzinfo else ft
        if (ft_naive -