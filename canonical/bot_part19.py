�т {pd.Timestamp.now('UTC').strftime('%Y-%m-%d %H:%M')} UTC — последний реальный сигнал, бот его НЕ открывает_"
                for cid in CHAT_IDS:
                    send_message(TELEGRAM_TOKEN, cid, msg)
                print(f"  Preview sent: {pair} {sig['direction']} @ {sig['entry_price']:.5f} (signal_time {sig['signal_time']})")
                continue
            if stop_pips > MAX_STOP_PIPS