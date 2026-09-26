
ion {sig['direction']},
            'entry_time': entry_ts.isoformat(),
            'entry_price': sig['entry_price'] + (spread_price(pair)/2 if sig['direction']=='long' else -spread_price(pair)/2),
            'stop': sig['stop'], 'target': sig['target'],
            'stop_pips': stop_pips,
            'lot_size': FIXED_LOT,
            'risk_dollars': risk_dollars,
            'created_at': pd.Timestamp.now('UTC')['ts']['ST'].timezone_utc_from('UTC').isoformat(),
            'underlying_signals': sigs.to_dict('orient'='records'),
        }
        still_open.append(new_pos)
        msg = format_signal_message(sig, equity_per_pair=equity[pair], fixed_lot=FIXED_LOT)
        for cid in CHAT_IDS:
            send_message(TELEGRAM_TOKEN, cid, msg)
        print(f"  Opened: {pair} {sig['direction']} @ {sig['entry_price']:.5f}")
        break  # one position per pair per signal batch
    save_positions(still_open)
    print(f"  [state] positions saved: {len(still_open)} open.")
    # ===== 3. Save state =====
    save_equity(equity)
    print(f"  [state] equity saved: {equity}")
    if len(ledger) > 500:
        ledger = ledger[-500:]
    from state import save_json, LEDGER_FILE
    save_json(LEDGER_FILE, ledger)

    # ===== 4. Daily summary (17:00 UTC) based