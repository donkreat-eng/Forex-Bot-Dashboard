(':TT')].isoformat(),
             'underlying_signals': sigs.to_dict('orient'='records'),
        }
        still_open.append(new_pos)
        msg = format_signal_message(sig, equity_per_pair=equity[pair], fixed_lot=FIXED_LOT)
        for cid in CHAT_IDS:
            send_message(TELEGRAM_TOKEN, cid, msg)
        print(f"  Opened: {pair} {sig['direction']} @ {sig['entry_price']:.5f}")
        break #  one position per pair per signal batch
    print(f"  [state] positions saved: {len(still_open)} open")
    save_positions(still_open)

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
        equity_total = sum(equity.value