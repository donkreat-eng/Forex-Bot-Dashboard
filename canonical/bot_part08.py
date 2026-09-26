o else ft).to_pydatetime()
        # Friday close rule
        if ft_py.weekday() == 4 and ft_py.hour >= FRIDAY_CLOSE_HOUR:
            pos['exit_time'] = ft
            pos['exit_price'] = fr['close']
            pos['exit_reason'] = 'friday_exit'
            return pos
        if pos['direction'] == 'long':
            if fr['low'] <= pos['stop']:
                pos['exit_time'] = ft
                pos['exit_price'] = pos['stop'] - spread