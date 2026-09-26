ay = json.load(f).get('date') == today.isoformat()
        except Exception:
            pass
        if now_utc.hour == HOLIDAY_NOTICE_HOUR_UTC and not sent_tlay:
            msg = f"Â����‍‏–‏ ил выходной — {reason}. Уорекс закрыт, торговля не ведётся, бот отдыхает."
            for cid in CHAT_IDS:
                send_message(TELEGRAM_TOKEN, cid, msg)
            try:
           