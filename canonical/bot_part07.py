= pos['pair']
    pip = pip_size(pair)
    df_idx = df_now.set_index('datetime')
    # Find bars from entry to now
    entry_t = pd.Timestamp(pos['entry_time']).tz_localize(None) if pd.Timestamp(pos['entry_time']).tzinfo else pd.Timestamp(pos['entry_time'])
    future = df_now[(df_now['datetime'] > entry_t)].reset_index(drop=True)
    for _, fr in future.iterrows():
        ft = fr['datetime']
        ft_py = (ft.tz_localize(None) if ft.tzinf