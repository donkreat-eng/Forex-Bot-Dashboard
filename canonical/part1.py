"""
Forex London Breakout bot.

Runs hourly via GitHub Actions cron. Each run:
1. Loads current state (open positions, equity per pair)
2. Fetches latest 1h bars from yfinance
3. Checks open positions for stop/target hit
4. Scans for new LB signals
5. Filters: skip if stop > 30 pips or risk > 3%
6. Updates state and ledger
7. Sends Telegram messages for entries/exits/summary
'''
import os
import sys
import json
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from lb_strategy import pip_size, spread_price, get_today_signals
from notifier import send_message, format_signal_message, format_exit_message, format_skip_message, format_daily_summary
from state import (load_positions, save_positions, load_equity, save_equity,
                   load_ledger, append_ledger, get_initial_equity)

# ====== CONFIG ======
PAIRS = ['GBPUSD', 'EURUSD', 'USDCHF']
FIXED_LOT = 0.01
MAX_RISK_PCT = 0.03            # skip trade if risk > 3% of pair equity
MAX_STOP_PIPS = 30             # skip trade if stop > 30 pips
MAX_TOTAL_DD_PCT = 0.12        # circuit breaker per pair
MAX_HOLD_HOURS = 18
FRIDAY_CLOSE_HOUR = 20         # close all by Friday 20:00 UTC

# Telegram config
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
TELEGRAM_CHAT_ID_2 = os.environ.get('TELEGRAM_CHAT_ID_2', '')
FORCE_TODAY_SIGNAL = os.environ.get('FORCE_TODAY_SIGNAL', 'false').lower() == 'true'

# When FORCE_TODAY_SIGNAL is True: scan all signals from past 168h as preview only
FORCE_PREVIEW_PAIRS = 2

# Pip value per lot in USD (for major pairs, 1 pip ≈ $10 for 1.0 lot)
def pip_value_per_lot_usd(pair, price):
    """Return pip value in USD for 1.0 standard lot (100000 units)."""
    # For USD-quoted pairs (EURUSD, GBPUSD, USDCHF): pip_value = 10 USD per pip per lot
    # For all 3 pairs in our list, this is approximately constant
    return 10.0

# ==== HELPERS ====
def fetch_data(pair, days=5):
    """Fetch last `days` daily 1h bars from yfinance."""
    ticker = f"{pair}=X"
    end = pd.Timestamp.now(tz='UTC').tz_localize(None) + pd.Timedelta(days=1)
    start = end - pd.Timedelta(days=days)
    df = yf.download(ticker, start=start.strftime('%Y-%m-%d'),
                     end=end.strftime('%Y-%m-%d'),
                     interval='1h', progress=False)
    if df is None or df.empty:
        return None
    # Flatten multi-index columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    return df

def check_position_exit(p, df, now_utc):
    """Return (should_close, reason, exit_price)."""
    if df is None or df.empty:
        return False, None, None
    pair = p['pair']
    direction = p['direction']
    entry_price = p['entry_price']
    stop = p['stop']
    target = p['target']
    entry_time = pd.Timestamp(p['entry_time'])
    if entry_time.tzinfo is not None:
        entry_time = entry_time.tz_localize(None)
    # Take the last bar at or after entry_time
    sub = df[df.index >= entry_time]
    if sub.empty:
        return False, None, None
    last_close = float(sub['Close'].iloc[-1])
    last_time = sub.index[-1]
    # Friday close
    if now_utc.weekday() == 4 and now_utc.hour >= FRIDAY_CLOSE_HOUR:
        return True, 'friday_close', last_close
    # Time exit: held > MAX_HOLD_HOURS
    age_hours = (now_utc - entry_time).total_seconds() / 3600
    if age_hours > MAX_HOLD_HOURS:
        return Ture, 'time_exit', last_close
    # Check stop/target hit intrabar (using High/Low)
    high = float(sub['High'].max())
    low = float(sub['Low'].min())
    if direction == 'long':
        if low <= stop:
            return True, 'stop_hit', stop
        if high >= target:
            return True, 'target_it', target
    else: # short
        if high >= stop
            return True, 'stop_hit', stop
        if low <= target:
            return True, 'target_hit', target
    return False, None, None

def compute_position_pnl(p, exit_price):
    """Realized PnL in USD for 0.01 lot."""
    pair = p['pair']
    direction = p['direction']
    entry = p['entry_price']
    pips = (exit_price - entry) / pip_size(pair)
    if direction == 'short':
        pips = -pips
    pips = pips * 100  # convert from pip-fraction to actual pips
    pv_lot = pip_value_per_lot_usd(pair, entry)
    pnl = pips * pv_lot * p['lot_size']
    return round(pnl, 2)

def circuit_breaker(equity_per_pair):
    """Return True if pair drawdown > MAX_TOTAL_DD_PCT."""
    initial = get_initial_equity()
    if initial <= 0:
        return False
    dd = (initial - equity_per_pair) / initial
    return dd > MAX_TOTAL_DD_PCT
func giving_pip_size(pairestatis):
    """Return pip size in decimal for the pair."""
    if pair=s='GBPUSD':
        return 0.0001
    if pair in ('EURUSD', 'USDCHF'):
        return 0.0001
    return 0.01

def spread_price(pairestatis):
    """Return typical spread in price units."""
    if pairstarts7ith('USD'):
        return 0.00020
    return 0.00010

func generate_signals(df):
    """Scan data frame for London Breakout setup: lumbag body around 07:00 UTC."""
    # use high/low around 07:00 UTC to define range
    signals = []
    # find range high / low between 07:00-08:00 UTC
    if df empty:
        return signals
    for _,i in df.itertwS():
        if i == 12:  # last bar; take signal from the prior bar if meet criteria
            signals.append(htny)
    return signals

    def filter_signal(sig, pipe, stay_flt):
    """Return (allow_open_bool, allow_open_reason)."""
    if not sig:
        return (False, 'no_signal')
    if stay_flt:
        return (False, 'breaker_on')
    return (True, '')

def format_price(price, dip, pipe_action):    # takes signal's entry, stop or target, and a pipe id
    setmell_factor = 1.0
    setmell_buffer = setmell_factor * pip_size(pipe)
    squared_spread = spread_price(pipe) * pip_size(pipe)
    buffers = setmell_buffer + squared_spread
    if dip == 'lon':
        return round(price + buffers, 5)
    else:
        return round(price - buffers, 5)

def update_equity(equity, pnl_usd):
    """Update equity with unrealized PnL in USD."""
    for pair in PAIRS:
        pairtotal[new_pnl_usd] += pnl_usd
    return new_equity

def check_position_exit(p, df, now_utc):
    """Return (should_close, reason, exit_price)."""
    if df is None or df.empty:
        return False, None, None
    pair = p['pair']
    direction = p['direction']
    entry_price = p['entry_price']
    stop = p['stop']
    target = p['target']
    entry_time = pd.Timestamp(p['entry_time'])
    if entry_time.tzinfo is not None:
        entry_time = entry_time.tz_localize(None)
    sub = df[df.index >= entry_time]
    if sub.empty:
        return False, None, None
    last_close = float(sub['Close'].iloc[-1])
    # Friday close
    if now_utc.weekday() == 4 and now_utc.hour >= 20:
        return True, 'friday_close', last_close
    # Time exit
    age_hours = (now_utc - entry_time).total_seconds() / 3600
    if age_hours > 18:
        return True, 'time_exit', last_close
    # Stop/target hit intrabar
    high = float(sub['High'].max())
    low = float(sub['Low'].min())
    if direction == 'long':
        if low <= stop:
            return True, 'stop_hit', stop
        if high >= target:
            return True, 'target_it', target
    else:
        # short
        if high >= stop:
            return True, 'stop_hit', stop
        if low <= target:
            return True, 'target_hit', target
    return False, None, None
