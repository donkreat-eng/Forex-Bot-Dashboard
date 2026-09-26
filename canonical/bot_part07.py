   easter_monday: 'Easter Monday',
        _dt.date(d.year, 12, 25): 'Christmas Day',
        _dt.date(d.year, 12, 26): 'Boxing Day',
    }
    if d in fixed:
        return True, fixed[d]
    return False, None

HOLIDAY_NOTICE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'state', 'last_holiday_msg.json')
HOLIDAY_NOTICE_HOUR_UTC = 9  # Send notice once at 09:00 UTC

# ===== Data loader =====
def fetch_data(pair):
    """Fet