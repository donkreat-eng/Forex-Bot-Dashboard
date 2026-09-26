=== CONFIG =====
PAIRS = ['GBPUSD', 'EURUSD', 'USDCHF']
FIXED_LOT = 0.01
MAX_RISK_PCT = 0.03          # skip trade if risk > 3% of pair equity
MAX_STOP_PIPS = 30           # skip trade if stop > 30 pips
MAX_TOTAL_DD_PCT = 0.12      # circuit breaker per pair
MAX_HOLD_HOURS = 18
FRIDAY_CLOSE_HOUR = 20       # close all by Friday 20:00 UTC

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID