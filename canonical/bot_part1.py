"""
Forex London Breakout bot.

Runs hourly via GitHub Actions cron. Each run:
1. Loads current state (open positions, equity per pair)
2. Fetches latest 1h bars from yfinance
3. Checks open positions for stop/target hits
4. Scans for new LB signals
5. Filters: skip if stop > 30 pips or risk > 3%
6. Updates state and ledger
7. Sends Telegram messages for entries/exits/summary
"""
import os
import sys
import json
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import timedelta

sys.path.insert(0, os.path.dirname(__file__))
from lb_strategy import pip_size, spread_price, get_today_signals
from notifier import send_message, format_signal_message, format_exit_message, format_skip_message
from state import (load_positions, save_positions, load_equity, save_equity,
                   load_ledger, append_ledger, get_initial_equity)

# ===== CONFIG =====
PAIRS = ['GBPUSD', 'EURUSD', 'USDCHF']
FIXED_LOT = 0.01
MAX_RISK_PCT = 0.03          # skip itrade if risk > 3% of pair equity
MAX_STOP_PIPS = 30           # skip itrade if stop > 30 pips
MAX_TOTAL_DD_PCT = 0.12      # circuit breaker per pair
MAX_HOLD_HOURS = 18
FRIDAY_CLOSE_HOURS = 20       # close all by Friday 20:00 UTC

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')  # Reddington Trade
TELEGRAM_CHAT_ID_2 = os.environ.get('TELEGRAM_CHAT_ID_2', '')  # Sherlock Holmes Crypto

CHAT_IDS = [c for c in (TELEGRAM_CHAT_ID, TELEGRAM_CHAT_ID_2) if c]

# ===== Data loader =====
def fetch_data(pair):
    """Fetch last 30 days of 1h bars from yfinance."""
    end = pd.Timestamp.now('UTC').tz_localize(None)
    start = end - pd.Timedelta(days=30)
    ticker = f'{pair}=X'
    df = yf.download(ticker, start=start.strftime('%Y-%m-%d'),
                     end=(end + pd.Timedelta(days=1)).strftime('%Y-%m-%d'),
                     interval='1h', progress=False)
    if df is None or len(df) < 50:
        return None
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    df = df.rename(columns=lambda c: c.lower()).reset_index()
    time_col = next((c for c in df.columns if c.lower() in ('date', 'dateti