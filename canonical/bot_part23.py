ill_open.append(new_pos)
            msg = format_signal_message(sig, equity_per_pair=equity[pair], fixed_lot=FIXED_LOT)
            for cid in CHAT_IDS:
                send_message(TELEGRAM_TOKEN, cid, msg)
            print(f"  Opened: {pair} {sig['direction']} @ {sig['entry_price']:.5f}")
            break  # one position per pair per signal batch
    save_positions(still_open)
    print(f"  [state] positions saved: {len(still_open)} open