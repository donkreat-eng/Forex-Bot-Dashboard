mary = pd.DataFrame(closed_today)
        msg = format_daily_summary(df_summary, equity_total)
        for cid in CHAT_IDS:
            send_message(TELEGRAM_TOKEN, cid, msg)

    print(f"\n=== Done. Open: {len(still_open)}, Closed today: {len(closed_today)} ===")
    print(f"Equity per pair: {equity}")
    return 0

if __name__ == '__main__':
    sys.exit(run())