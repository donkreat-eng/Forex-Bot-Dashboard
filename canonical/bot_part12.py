xit_reason'] = 'friday_exit'
            return pos
        if pos['direction'] == 'long':
            if fr['low'] <= pos['stop']:
                pos['exit_time'] = ft
                pos['exit_price'] = pos['stop'] - spread_price(pair) / 2
                pos['exit_reason'] = 'stop'
                return pos
            if fr['high'] >= pos['target']:
                pos['exit_time'] = ft
                pos['exit_price'] = pos['target'] 