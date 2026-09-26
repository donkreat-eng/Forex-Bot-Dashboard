 MAX_RISK_PCT:
                skip_msg = format_skip_message(sig, f"риск {risk_pct*100:.1f}% > лимит {MAX_RISK_PCT*100:.0f}%")
                for cid in CHAT_IDS:
                    send_message(TELEGRAM_TOKEN, cid, skip_msg)
                continue
            # Open position
            entry_bar = df[df['datetime'] >= sig['signal_time']].iloc[0]
            entry_ts = entry_bar['datetime']
            new_pos = {
             