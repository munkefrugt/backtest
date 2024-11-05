
# stats.py
import numpy as np

def update_streak(simulator, profit):
    if profit > 0:
        if simulator.current_streak_type == 'win':
            simulator.winning_streak += 1
        else:
            simulator.winning_streak = 1
            simulator.losing_streak = 0
        simulator.current_streak_type = 'win'
    else:
        if simulator.current_streak_type == 'loss':
            simulator.losing_streak += 1
        else:
            simulator.losing_streak = 1
            simulator.winning_streak = 0
        simulator.current_streak_type = 'loss'

    simulator.max_winning_streak = max(simulator.max_winning_streak, simulator.winning_streak)
    simulator.max_losing_streak = max(simulator.max_losing_streak, simulator.losing_streak)


def get_stats(simulator):
    num_trades = len(simulator.profits)
    num_wins = len([p for p in simulator.profits if p > 0])
    win_rate = num_wins / num_trades if num_trades > 0 else 0
    avg_profit = np.mean(simulator.profits) if simulator.profits else 0
    max_drawdown = max(simulator.drawdowns) if simulator.drawdowns else 0
    avg_percentage_gain = np.mean(simulator.percentage_gains) if simulator.percentage_gains else 0

    return {
        "win_rate": win_rate,
        "average_profit": avg_profit,
        "max_drawdown": max_drawdown,
        "average_percentage_gain_per_trade": avg_percentage_gain,
        "max_winning_streak": simulator.max_winning_streak,
        "max_losing_streak": simulator.max_losing_streak
    }


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

