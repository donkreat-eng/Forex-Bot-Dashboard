     os.makedirs(os.path.dirname(HOLIDAY_NOTICE_FILE), exist_ok=True)
                with open(HOLIDAY_NOTICE_FILE, 'w') as f:
                    json.dump({'date': today.isoformat(), 'reason': reason}, f)
            except Exception as e:
                print(f"[warn] could not save holiday marker: {e}")
            print(f"[holiday] {today} {reason} — notice sent")
        elif sent_today:
            print(f"[holiday] {today} {reason