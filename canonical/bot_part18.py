l_open):
                continue
            # Risk filters
            pip = pip_size(pair)
            stop_pips = abs(sig['entry_price'] - sig['stop']) / pip
            # Preview mode: post the historical signal as preview without opening position
            if force_preview:
                msg = format_signal_message(sig, equity_per_pair=equity[pair], fixed_lot=FIXED_LOT)
                msg += f"\n\n_⚠️ ПРЕДПРОСМОТР �