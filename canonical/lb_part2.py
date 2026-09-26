a_low
        if a_range < min_range_pips * pip: continue
        london_bars = df[(df['date'] == d) & (df['hour'].isin([7, 8]))]
        if len(london_bars) == 0: continue
        # Skip Friday
        if london_bars.iloc[0]['datetime'].weekday() == 4: continue
        for _, bar in london_bars.iterrows():
            if bar['high'] > a_high + pip:
                sigs.append({
                    'pair': pair, 'signal_time': bar['datetime'],
                    'direction': 'long', 'entry_price': a_high + pip,
                    'stop': a_low - pip, 'target': a_high + pip + a_range * 1.5,
                    'asian_range_pips': a_range / pip,
                })
                break
            elif bar['low'] < a_low - pip:
                sigs.append({
                    'pair': pair, 'signal_time': bar['datetime'],
                    'direction': 'short', 'entry_price': a_low - pip,
                    'stop': a_high + pip, 'target': a_low - pip - a_range * 1.5,
               