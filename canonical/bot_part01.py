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
import num