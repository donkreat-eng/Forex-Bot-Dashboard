
    pos['duration_hours'] = (pd.Timestamp(pos['exit_time']) - pd.Timestamp(pos['entry_time'])).total_seconds() / 3600
    return pos

# ===== Main bot logic =====
def run():
    print(f"=== Forex Breakout Bot — {pd.Timestamp.now('UTC').isoformat()} ===")
    positions = load_positions()
    equity = load_equity()
    ledger = load_ledger()
    closed_today = []
    initial_equity = get_initial_equity('EURUSD')

    # Initialize equity per 