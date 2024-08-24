import plotly.graph_objs as go
import plotly.subplots as sp
import pandas as pd

def plot_backtest(df, buy_signals, sell_signals, cash_equity_df):
    # Ensure timestamp is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Create subplots
    fig = sp.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02,
                           subplot_titles=('Price & Indicators', 'Equity Curve', 'Cash Curve'))

    # Plot price data
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close_price'], mode='lines', name='Close Price', line=dict(color='blue')), row=1, col=1)

    # Plot resistance levels
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Resistance'], mode='lines', name='Resistance', line=dict(color='green', dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Support'], mode='lines', name='Support', line=dict(color='red', dash='dash')), row=1, col=1)

    # Plot EMAs
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['EMA_200'], mode='lines', name='EMA 200', line=dict(color='brown')), row=1, col=1)

    # Plot Donchian Channels
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Donchian_5_low'], mode='lines', name='Donchian 5 Low', line=dict(color='green', dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Donchian_10_low'], mode='lines', name='Donchian 10 Low', line=dict(color='cyan', dash='dash')), row=1, col=1)

    # Plot buy signals
    for signal in buy_signals:
        fig.add_trace(go.Scatter(x=[signal[0]], y=[signal[1]], mode='markers', name='Buy Signal', marker=dict(color='green', symbol='triangle-up', size=10)), row=1, col=1)
    
    # Plot sell signals
    for signal in sell_signals:
        fig.add_trace(go.Scatter(x=[signal[0]], y=[signal[1]], mode='markers', name='Sell Signal', marker=dict(color='red', symbol='triangle-down', size=10)), row=1, col=1)

    # Plot equity curve
    if not pd.api.types.is_datetime64_any_dtype(cash_equity_df['timestamp']):
        cash_equity_df['timestamp'] = pd.to_datetime(cash_equity_df['timestamp'])
        
    fig.add_trace(go.Scatter(x=cash_equity_df['timestamp'], y=cash_equity_df['equity'], mode='lines', name='Equity Curve', line=dict(color='black')), row=2, col=1)

    # Plot cash curve
    fig.add_trace(go.Scatter(x=cash_equity_df['timestamp'], y=cash_equity_df['cash'], mode='lines', name='Cash Curve', line=dict(color='red')), row=3, col=1)

    # Update layout
    fig.update_layout(height=800, width=1200, title_text='Backtest Results', showlegend=True)

    # Show plot
    fig.show()
