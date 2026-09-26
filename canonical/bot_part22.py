   'pair': pair, 'direction': sig['direction'],
                'entry_time': entry_ts.isoformat(),
                'entry_price': sig['entry_price'] + (spread_price(pair)/2 if sig['direction']=='long' else -spread_price(pair)/2),
                'stop': sig['stop'], 'target': sig['target'],
                'stop_pips': stop_pips,
                'lot_size': FIXED_LOT,
                'risk_dollars': risk_dollars,
            }
            still_open.append(new_pos)
            msg = format_signal_message(sig, equity_per_pair=equity[pair], fixed_lot=FIXED_LOT)
            for cid in CHAT_IDS:
                send_message(TELEGRAM_TOKEN, cid, msg)
            print(f"  Opened: {pair} {sig['direction']} @ {sig['entry_price']:.5f}")
            break  # one position per pair per signal batch
    save_positions(still_open)
    print(f"  [state] positions saved: {len(still_open)} open")

    # ====== 3. Save state ======
    save_equity(equity)
    print(f"  [state] equity saved: {equity}")
    # Save ledger (keep last 500)
    if len(ledger) > 500:
        ledger = ledger[-500:]
    from state import save_json, LEDGER_FILE
    save_json(LEDGER_FILE, ledger)

    # ===== 4. Daily summary at end of London day (17:00 UTC) =====
    if pd.Timestamp.now('UTC').tz_localize(None).hour == 17:
        equity_total = sum(equity.values())
        from notifier import format_daily_summary
        df_summary = pd.DataFrame(closed_today)
        msg = format_daily_summary(df_summary, equity_total)
        for cid in CHAT_IDS:
            send_message(TELEGRAM_TOKEN, cid, msg)

    print(f"\n=== Done. Open: {len(still_open)}, Closed today: {len(closed_today)} ===")
    print(f"Equity per pair: {equity}")
    return 0

if __name__ == '__main__':
    sys.exit(run())