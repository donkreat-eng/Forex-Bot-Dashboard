:
                skip_msg = format_skip_message(sig, f"stop {stop_pips:.1f} пипс > лимит {MAX_STOP_PIPS}")
                for cid in CHAT_IDS:
                    send_message(TELEGRAM_TOKEN, cid, skip_msg)
                continue
            pv_lot = pip_value_per_lot_usd(pair, sig['entry_price'])
            risk_dollars = stop_pips * pv_lot * FIXED_LOT
            risk_pct = risk_dollars / equity[pair]
            if risk_pct >