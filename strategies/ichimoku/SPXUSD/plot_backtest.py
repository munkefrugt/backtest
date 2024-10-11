import plotly.graph_objs as go
import plotly.subplots as sp
import pandas as pd

def plot_backtest(df, buy_signals, sell_signals, cash_equity_df):
    # Ensure date is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'])

    # Ensure the same for cash_equity_df dates
    if not pd.api.types.is_datetime64_any_dtype(cash_equity_df['date']):
        cash_equity_df['date'] = pd.to_datetime(cash_equity_df['date'])

    # Remove weekends from both df and cash_equity_df
    df = df[df['date'].dt.weekday < 5]
    cash_equity_df = cash_equity_df[cash_equity_df['date'].dt.weekday < 5]

    # Create subplots with shared x-axis for all rows
    fig = sp.make_subplots(
        rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.02,
        subplot_titles=('Price & Indicators', 'Equity Curve', 'Cash Curve', 'EMA Slopes')
    )

    # Plot price data (first subplot)
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines', name='Close Price', line=dict(color='dodgerblue')), row=1, col=1)

    # Plot Donchian Channels (optional first subplot)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_20_high'], mode='lines', name='DC 20 High', line=dict(color='purple')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_10_low'], mode='lines', name='DC 10 Low', line=dict(color='pink')), row=1, col=1)

    # Plot EMAs (first subplot)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_50'], mode='lines', name='EMA 50', line=dict(color='yellow')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_200'], mode='lines', name='EMA 200', line=dict(color='lightblue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_1000'], mode='lines', name='EMA 1000', line=dict(color='pink')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_5000'], mode='lines', name='EMA 5000', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_20000'], mode='lines', name='EMA 20000', line=dict(color='orange')), row=1, col=1)

    # Plot Ichimoku Base Line and Conversion Line (first subplot)
    fig.add_trace(go.Scatter(x=df['date'], y=df['ichimoku_base_line'], mode='lines', name='Ichimoku Base Line', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['ichimoku_conversion_line'], mode='lines', name='Ichimoku Conversion Line', line=dict(color='blue')), row=1, col=1)

    # Plot Ichimoku Cloud
    fig.add_trace(go.Scatter(x=df['date'], y=df['ichimoku_a'], mode='lines', line=dict(color='rgba(0, 0, 0, 0)'), showlegend=True, name='Ichimoku Cloud'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['ichimoku_b'], mode='lines', fill='tonexty', fillcolor='rgba(169, 169, 169, 0.5)', showlegend=False), row=1, col=1)

    # Corrected Chikou Line (shifted 26 periods forward)
    fig.add_trace(go.Scatter(x=df['date'], y=df['chikou_26_past'].shift(-26), mode='lines', name='Chikou Line', line=dict(color='pink')), row=1, col=1)

    # Plot buy signals (first subplot)
    fig.add_trace(go.Scatter(
        x=[signal[0] for signal in buy_signals], 
        y=[signal[1] for signal in buy_signals], 
        mode='markers', name='Buy Signal', 
        marker=dict(color='lime', symbol='triangle-up', size=10)
    ), row=1, col=1)

    # Plot sell signals (first subplot)
    fig.add_trace(go.Scatter(
        x=[signal[0] for signal in sell_signals], 
        y=[signal[1] for signal in sell_signals], 
        mode='markers', name='Sell Signal', 
        marker=dict(color='red', symbol='triangle-down', size=10)
    ), row=1, col=1)

    # Plot equity curve (second subplot)
    fig.add_trace(go.Scatter(x=cash_equity_df['date'], y=cash_equity_df['equity'], mode='lines', name='Equity Curve', line=dict(color='white')), row=2, col=1)

    # Plot cash curve (third subplot)
    fig.add_trace(go.Scatter(x=cash_equity_df['date'], y=cash_equity_df['cash'], mode='lines', name='Cash Curve', line=dict(color='yellow')), row=3, col=1)

    # Plot EMA slopes (fourth subplot)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_50_slope'], mode='lines', name='EMA 50 Slope', line=dict(color='yellow')), row=4, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_200_slope'], mode='lines', name='EMA 200 Slope', line=dict(color='lightblue')), row=4, col=1)

    # Update layout to make sure the x-axis is categorical and aligned across all subplots
    fig.update_layout(
        height=1200, width=1200, title_text='Backtest Results with Everything', 
        showlegend=True, template='plotly_dark',
    )
    
    # Ensure that all subplots share the same x-axis type (categorical)
    fig.update_xaxes(type='category')  # Apply category type to all x-axes

    # Show plot
    fig.show()

# Example usage: assuming df, buy_signals, sell_signals, and cash_equity_df are defined
# plot_backtest(df, buy_signals, sell_signals, cash_equity_df)
