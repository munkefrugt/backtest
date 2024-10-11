# Compare buy-and-hold strategy with backtested strategy
def buy_and_hold_compare_equity(df, cash_equity_df, initial_cash=1000):
    first_price = df['close'].iloc[0]
    last_price = df['close'].iloc[-1]
    first_equity = cash_equity_df['equity'].iloc[0]
    last_equity = cash_equity_df['equity'].iloc[-1]

    bought = initial_cash / first_price
    final_value = bought * last_price

    percentage_gain_buy_hold = ((final_value - initial_cash) / initial_cash) * 100
    percentage_gain_equity = ((last_equity - first_equity) / first_equity) * 100
    print(f"buy and hold % Gain: {percentage_gain_buy_hold:.2f}%")
    print(f"equity % Gain: {percentage_gain_equity:.2f}%")

