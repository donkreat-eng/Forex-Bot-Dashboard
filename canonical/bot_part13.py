- spread_price(pair) / 2
                pos['exit_reason'] = 'target'
                return pos
        else:
            if fr['high'] >= pos['stop']:
                pos['exit_time'] = ft
                pos['exit_price'] = pos['stop'] + spread_price(pair) / 2
                pos['exit_reason'] = 'stop'
                return pos
            if fr['low'] <= pos['target']:
                pos['exit_time'] = ft
                pos['exit_pri