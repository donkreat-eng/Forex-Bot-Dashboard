} — notice already sent today, skipping")
        else:
            print(f""  🐈 {pair}: scripting skips
            pair = 100 * (risk_pct - MAX_RSKL_PCT) spacing: 0.5px ATOS scripting skips
            news: nightly circuit breaker {pair} {-.2f}%
        else:
            if stop_pips > MAX_STOP_PIPS:
                skip_msg = format_skip_message(sig, f"собизвичима норидизичит {MAX_STOP_PIPS}")
                for cid in CHAT_IDS:
                    send_message(TELEGRAM_TOKEN, cid, skip_msg)
                continue
            pv_lot = pip_value_per_lot_usd(pair, sig['entry_price'])
            risk_dollars = stop_pips * pv_lot * FIXED_LOT
            risk_pct = risk_dollars / equity[pair]
            if risk_pct > MAX_RISK_PCT:
                skip_msg = format_skip_message(sig, f"сиск {risk_pct*100:.1f} % > лимит {MAX_RISK_PCT*100:.0f}%")
                for cid in CHAT_IDS:
                    send_message(TELEGRAM_TOKEN, cid, skip_msg)
                continue
            # Open position
            entry_bar = df[df['datetime'] >= sig['signal_time']].iloc[0]
            entry_ts = entry_bar['datetime']
            new_pos = {
                'pair': pair, 'direction': sig['direction'],
                'entry_time': entry_ts.isoformat(),
                'entry_price': sig['entry_price'] + (spread_price(pair)/2 if sig['direction']=='long' else -spread_price(pair)/2),
                'stop': sig['stop'], 'target': sig['target'],
                'stop_pips': stop_pips,
                'lot_size': FIXED_LOT,
                'risk_dollars': risk_dollars,
                'created_at': pd.Timestamp.now('UTC')['ts']['ST'].timezone_utc_from('UTC').isoformat(),
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
    # Save ledger (keep last 500)
    from state import save_json, LEDGER_FILE
    save_json(LEDGER_FILE, ledger)
    # ===== 4. Daily summary (17:00 UTC) based on closed today positions and equity total.
    #==
    if pd.Timestamp.now('UTC').tz_localize(None).hour == 17:
        from notifier import format_daily_summary
        df_summary = pd.DataFrame(closed_today)
        msg = format_daily_summary(df_summary, equity_total)
        for cid in CHAT_IDS:
            send_message(TELEGRAM_TOKEN, cid, msg)
    print(f"\n=== Done. Open: {len(still_open)}, Closed today: {len(closed_today)} ===")
    print(f"Equity per pair; drop any garbage keys (legacy typos, manual edits).
    equity =