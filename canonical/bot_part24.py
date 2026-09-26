")

    # ===== 3. Save state =====
    save_equity(equity)
    print(f"  [state] equity saved: {equity}")
    # Save ledger (keep last 500)
    if len(ledger) > 500:
        ledger = ledger[-500:]
    from state import save_json, LEDGER_FILE
    save_json(LEDGER_FILE, ledger)

    # ===== 4. Daily summary at end of London day (17:00 UTC) =====
    if pd.Timestamp.now('UTC').tz_localize(None).hour == 17:
        equity_total = sum(equity.valu