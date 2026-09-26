 on closed today positions and equity total.
        equity_total = sum(equity.values())
        from notifier import format_daily_summary
        dds = [pos['created_at'] for pos in closed_today if 'pnl' in pos]
        df_summary = pd.DataFrame(dds[:][:5], columns=['pair','direction','pnl','r_multiple']) if dds else pd.DataFrame(columns='req