ice):
    pip = pip_size(pair)
    return (pip / price) * 100000

# ===== Position management =====
def check_position_exit(pos, df_now):
    """Check if open position hit stop/target. Returns updated pos or None."""
    pair = pos['pair']
    pip = pip_size(pair)
    df_idx = df_now.set_index('datetime')
    # Find bars from entry to now
    entry_t = pd.Timestamp(pos['entry_time']).tz_localize(None) if pd.Timestamp(pos['entry_time']).tzinfo