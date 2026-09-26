py as np
import yfinance as yf
from datetime import timedelta

sys.path.insert(0, os.path.dirname(__file__))
from lb_strategy import pip_size, spread_price, get_today_signals
from notifier import send_message, format_signal_message, format_exit_message, format_skip_message
from state import (load_positions, save_positions, load_equity, save_equity,
                   load_ledger, append_ledger, get_initial_equity)

# ===== CONFIG =====
PAIRS 