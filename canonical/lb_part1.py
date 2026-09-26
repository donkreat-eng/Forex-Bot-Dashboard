"""
London Breakout strategy for forex pairs.
Generates entry signals based on Asian range breakout at London open (07-09 UTC).
"""
import pandas as pd
import numpy as np

def pip_size(pair):
    return 0.01 if 'JPY' in pair else 0.0001

def spread_price(pair, slippage_pips=0.2):
    """Realistic retail spreads + slippage, in price units."""
    spreads = {'EURUSD': 0.6, 'GBPUSD': 0.9, 'USDCHF': 1.0, 'USDJPY': 0.7, 'AUDUSD': 1.0}
    return (spreads[pair] + slippage_pips) * pip_size(pair)

def generate_signals(df, pair, min_range_pips=8):
    """Generate LB entry signals from 1h OHLC dataframe."""
    pip = pip_size(pair)
    sigs = []
    df = df.copy()
    df['date'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    dates = sorted(df['date'].unique())
    for d in dates[:-1]:
        asian = df[(df['date'] == d) & (df['hour'] < 7)]
        if len(asian) < 4: continue
        a_high = asian['high'].max()
        a_low = asian['low'].min()
        a_range = a_high - 