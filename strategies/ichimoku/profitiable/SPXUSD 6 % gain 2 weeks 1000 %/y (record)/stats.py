# stats.py
import numpy as np
from datetime import datetime

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

def calculate_trade_durations(trades):
    durations = []
    for trade in trades:
        if trade.status == 'closed':  # Only consider closed trades
            duration_hours = (trade.close_time - trade.buy_time).total_seconds() / 3600
            durations.append(duration_hours)
    return durations

def get_average_trade_duration(trades):
    durations = calculate_trade_durations(trades)
    return np.mean(durations) if durations else 0  # Return 0 if no closed trades

def projected_annualized_return(avg_gain_per_trade, avg_trade_duration_hours, win_rate, loss_rate, trade_frequency_per_year, downtime_factor):
    expected_return_per_trade = (avg_gain_per_trade * win_rate) - (loss_rate * (1 - win_rate))
    effective_trade_cycles_per_year = trade_frequency_per_year * (1 - downtime_factor)
    annualized_return = (1 + expected_return_per_trade) ** effective_trade_cycles_per_year - 1
    return annualized_return * 100  # Convert to percentage

def get_projected_annualized_returns(simulator):
    if simulator.percentage_gains:
        avg_gain_per_trade = np.mean([gain for gain in simulator.percentage_gains if gain > 0]) / 100
        loss_rate = -np.mean([gain for gain in simulator.percentage_gains if gain < 0]) / 100 if any(g < 0 for g in simulator.percentage_gains) else 0
    else:
        avg_gain_per_trade = 0
        loss_rate = 0

    avg_trade_duration_hours = get_average_trade_duration(simulator.trades)
    win_rate = len([p for p in simulator.profits if p > 0]) / len(simulator.profits) if simulator.profits else 0
    trade_frequency_per_year = len(simulator.trades)  # Assuming backtest is over 1 year

    # Downtime scenarios
    downtime_scenarios = {
        "0% Not in Trade": 0.0,
        "1% Not in Trade": 0.01,
        "10% Not in Trade": 0.1,
        "50% Not in Trade": 0.5
    }

    # Calculate projected annualized returns for each scenario
    projected_returns = {}
    for scenario, downtime in downtime_scenarios.items():
        if avg_gain_per_trade > 0 and avg_trade_duration_hours > 0:
            projected_returns[scenario] = projected_annualized_return(
                avg_gain_per_trade, avg_trade_duration_hours, win_rate, loss_rate, trade_frequency_per_year, downtime
            )
        else:
            projected_returns[scenario] = 0

    return projected_returns

def calculate_max_drawdown(equity_curve):
    """
    Calculate the maximum drawdown from the equity curve.
    """
    running_max = np.maximum.accumulate(equity_curve)
    drawdowns = (running_max - equity_curve) / running_max
    max_drawdown = np.max(drawdowns) * 100  # Convert to percentage
    return max_drawdown

def get_stats(simulator, cash_equity_df):
    num_trades = len(simulator.profits)
    num_wins = len([p for p in simulator.profits if p > 0])
    win_rate = num_wins / num_trades * 100 if num_trades > 0 else 0  # Convert to percentage
    avg_profit = np.mean(simulator.profits) if simulator.profits else 0
    avg_percentage_gain = np.mean(simulator.percentage_gains) if simulator.percentage_gains else 0  # Already in percentage
    avg_trade_duration = get_average_trade_duration(simulator.trades)

    # Use the equity curve from cash_equity_df to calculate max drawdown
    equity_curve = cash_equity_df['equity'].values  # Extract equity values as a numpy array
    max_drawdown = calculate_max_drawdown(equity_curve) if len(equity_curve) > 0 else 0

    # Calculate percentage gain per minute, per hour, and per day
    avg_trade_duration_minutes = avg_trade_duration * 60  # Convert hours to minutes
    avg_trade_duration_days = avg_trade_duration / 24     # Convert hours to days
    gain_per_minute = (avg_percentage_gain / avg_trade_duration_minutes) if avg_trade_duration_minutes else 0
    gain_per_hour = (avg_percentage_gain / avg_trade_duration) if avg_trade_duration else 0
    gain_per_day = (avg_percentage_gain / avg_trade_duration_days) if avg_trade_duration_days else 0

    # Calculate benchmark daily gain to beat a 7% annual return
    target_annual_return = 0.07
    trading_days_per_year = 252
    benchmark_daily_gain = ((1 + target_annual_return) ** (1 / trading_days_per_year) - 1) * 100

    # Get projected returns for downtime scenarios and convert to percentages
    projected_annualized_returns = {scenario: value * 100 for scenario, value in get_projected_annualized_returns(simulator).items()}

    # Prepare the statistics dictionary with readable formatting
    stats = {
        "Win Rate (%)": f"{win_rate:.2f}",
        "Average Profit (USD)": f"{avg_profit:.2f}",
        "Max Drawdown (%)": f"{max_drawdown:.2f}",
        "Avg Percentage Gain per Trade (%)": f"{avg_percentage_gain:.2f}",
        "Max Winning Streak": f"{simulator.max_winning_streak}",
        "Max Losing Streak": f"{simulator.max_losing_streak}",
        "Avg Trade Duration (hours)": f"{avg_trade_duration:.2f}",
        "Percentage Gain per Minute (%)": f"{gain_per_minute:.4f}",
        "Percentage Gain per Hour (%)": f"{gain_per_hour:.4f}",
        "Percentage Gain per Day (%)": f"{gain_per_day:.4f}",
        "Benchmark Daily Gain for 7% Annual Return (%)": f"{benchmark_daily_gain:.4f}",  # Benchmark
        **{f"{scenario} Annualized Return (%)": f"{value:.2f}" for scenario, value in projected_annualized_returns.items()}
    }

    # Print each stat with alignment for readability
    print("\nBacktest Summary:\n" + "-"*30)
    for stat, value in stats.items():
        print(f"{stat:<40}: {value}")
    print("\n")  # Extra newline for spacing at the end

    return stats


def buy_and_hold_compare_equity(df, cash_equity_df, initial_cash=1000):
    first_price = df['close'].iloc[0]
    last_price = df['close'].iloc[-1]
    first_equity = cash_equity_df['equity'].iloc[0]
    last_equity = cash_equity_df['equity'].iloc[-1]

    bought = initial_cash / first_price
    final_value = bought * last_price

    percentage_gain_buy_hold = ((final_value - initial_cash) / initial_cash) * 100
    percentage_gain_equity = ((last_equity - first_equity) / first_equity) * 100
    print(f"Buy and Hold % Gain: {percentage_gain_buy_hold:.2f}%")
    print(f"Equity % Gain: {percentage_gain_equity:.2f}%")
