     'asian_range_pips': a_range / pip,
                })
                break
    return pd.DataFrame(sigs)

def get_today_signals(df, pair, now=None, lookback_hours=None):
    """Only signals from last 18 hours (or last 7 days if FORCE_TODAY_SIGNAL=true/1/yes)."""
    import os
    sigs = generate_signals(df, pair)
    if len(sigs) == 0: return sigs
    # Use naive UTC to avoid tz-naive vs tz-aware comparison error
    if lookback_hours is None:
        if os.environ.get('FORCE_TODAY_SIGNAL', '').lower() in ('1', 'true', 'yes'):
            lookback_hours = 168  # 7 days
        else:
            lookback_hours = 18
    if now is None:
        now = pd.Timestamp.now('UTC')
    cutoff = now.tz_localize(None) - pd.Timedelta(hours=lookback_hours) if now.tz is not None else now - pd.Timedelta(hours=lookback_hours)
    sigs_t = pd.to_datetime(sigs['signal_time']).dt.tz_localize(None)
    return sigs[sigs_t >= cutoff].reset_index(drop=True)