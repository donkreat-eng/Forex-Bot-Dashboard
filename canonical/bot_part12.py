info else pd.Timestamp(pos['entry_time'])
    future = df_now[(df_now['datetime'] > entry_t)].reset_index(drop=True)
    for _, fr in future.iterrows():
        ft = fr['datetime']
        ft_py = (ft.tz_localize(None) if ft.tzinfo else ft).to_pydatetime()
        # Friday close rule
        if ft_py.weekday() == 4 and ft_py.hour >= FRIDAY_CLOSE_HOUR:
            pos['exit_time'] = ft
            pos['exit_price'] = fr['close']
            po