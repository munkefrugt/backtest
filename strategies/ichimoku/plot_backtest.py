import plotly.graph_objs as go
import plotly.subplots as sp
import pandas as pd

def plot_backtest(df, buy_signals, sell_signals, cash_equity_df):
    # Ensure date is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'])

    # Create subplots
    fig = sp.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02,
                           subplot_titles=('Price & Indicators', 'Equity Curve', 'Cash Curve'))

    # Plot price data
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines', name='Close Price', line=dict(color='dodgerblue')), row=1, col=1)

    # Plot Donchian Channels (legends enabled)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_20_high'], mode='lines', name='DC 20 High', line=dict(color='purple')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_10_low'], mode='lines', name='DC 10 Low', line=dict(color='pink')), row=1, col=1)

    # Plot EMAs (legends enabled)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_50'], mode='lines', name='EMA 50', line=dict(color='yellow')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_200'], mode='lines', name='EMA 200', line=dict(color='lightblue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_1000'], mode='lines', name='EMA 1000', line=dict(color='pink')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_5000'], mode='lines', name='EMA 5000', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_20000'], mode='lines', name='EMA 20000', line=dict(color='orange')), row=1, col=1)

    # Plot Ichimoku Base Line and Conversion Line (legends enabled)
    fig.add_trace(go.Scatter(x=df['date'], y=df['ichimoku_base_line'], mode='lines', name='Ichimoku Base Line', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['ichimoku_conversion_line'], mode='lines', name='Ichimoku Conversion Line', line=dict(color='lightblue')), row=1, col=1)

    # Plot Ichimoku Chikou Line (legend enabled)
    fig.add_trace(go.Scatter(x=df['date'], y=df['ichimoku_chikou_line'], mode='lines', name='Ichimoku Chikou Line', line=dict(color='pink')), row=1, col=1)

    # Separate clouds for Senkou Span A > Senkou Span B (green) and Senkou Span B > Senkou Span A (red)
    green_cloud = df[df['ichimoku_a'] >= df['ichimoku_b']]
    red_cloud = df[df['ichimoku_b'] > df['ichimoku_a']]

    # Green cloud: A > B
    fig.add_trace(go.Scatter(
        x=green_cloud['date'], y=green_cloud['ichimoku_a'],
        mode='lines', line=dict(color='rgba(0, 0, 0, 0)'),  # No visible line
        showlegend=True, name='Ichimoku Cloud (Green)', fill=None
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=green_cloud['date'], y=green_cloud['ichimoku_b'],
        mode='lines', line=dict(color='rgba(0, 0, 0, 0)'),
        fill='tonexty', fillcolor='rgba(0, 255, 0, 0.3)',  # Green fill
        showlegend=False
    ), row=1, col=1)

    # Red cloud: B > A
    fig.add_trace(go.Scatter(
        x=red_cloud['date'], y=red_cloud['ichimoku_a'],
        mode='lines', line=dict(color='rgba(0, 0, 0, 0)'),  # No visible line
        showlegend=True, name='Ichimoku Cloud (Red)', fill=None
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=red_cloud['date'], y=red_cloud['ichimoku_b'],
        mode='lines', line=dict(color='rgba(0, 0, 0, 0)'),
        fill='tonexty', fillcolor='rgba(255, 0, 0, 0.3)',  # Red fill
        showlegend=False
    ), row=1, col=1)

    # Plot buy signals (Green) with legend
    fig.add_trace(go.Scatter(
        x=[signal[0] for signal in buy_signals], 
        y=[signal[1] for signal in buy_signals], 
        mode='markers', name='Buy Signal', 
        marker=dict(color='lime', symbol='triangle-up', size=10)
    ), row=1, col=1)

    # Plot sell signals (Red) with legend
    fig.add_trace(go.Scatter(
        x=[signal[0] for signal in sell_signals], 
        y=[signal[1] for signal in sell_signals], 
        mode='markers', name='Sell Signal', 
        marker=dict(color='red', symbol='triangle-down', size=10)
    ), row=1, col=1)

    # Plot equity curve (legend enabled)
    if not pd.api.types.is_datetime64_any_dtype(cash_equity_df['date']):
        cash_equity_df['date'] = pd.to_datetime(cash_equity_df['date'])
        
    fig.add_trace(go.Scatter(x=cash_equity_df['date'], y=cash_equity_df['equity'], mode='lines', name='Equity Curve', line=dict(color='white')), row=2, col=1)

    # Plot cash curve (legend enabled)
    fig.add_trace(go.Scatter(x=cash_equity_df['date'], y=cash_equity_df['cash'], mode='lines', name='Cash Curve', line=dict(color='yellow')), row=3, col=1)

    # Update layout with dark theme
    fig.update_layout(height=800, width=1200, title_text='Backtest Results', showlegend=True, template='plotly_dark')

    # Show plot
    fig.show()
