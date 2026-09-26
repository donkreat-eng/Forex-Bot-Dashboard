')), None)
    df['datetime'] = pd.to_datetime(df[time_col]).dt.tz_localize(None)
    return df[['datetime','open','high','low','close']].sort_values('datetime').reset_index(drop=True)

def pip_value_per_lot_usd(pair, price):
    pip = pip_size(pair)
    return (pip / price) * 100000

# ===== Position management =====
def check_position_exit(pos, df_now):
    """Check if open position hit stop/target. Returns updated pos or None."""
    pair