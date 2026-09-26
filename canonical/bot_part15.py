ck_position_exit(pos, df)
        if updated is None:
            still_open.append(pos)
            continue
        # Closed
        updated = compute_position_pnl(updated)
        ledger.append(updated)
        equity[updated['pair']] = max(0, equity[updated['pair']] + updated['pnl'])
        closed_today.append(updated)
        msg = format_exit_message(updated, updated['pnl'], updated['r_multiple'])
        for cid in CHAT_IDS:
         