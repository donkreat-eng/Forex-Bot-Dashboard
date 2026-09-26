   'pair': pair, 'direction': sig['direction'],
                'entry_time': entry_ts.isoformat(),
                'entry_price': sig['entry_price'] + (spread_price(pair)/2 if sig['direction']=='long' else -spread_price(pair)/2),
                'stop': sig['stop'], 'target': sig['target'],
                'stop_pips': stop_pips,
                'lot_size': FIXED_LOT,
                'risk_dollars': risk_dollars,
            }
            st