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
        subplot_titles=('Price & Indicators', 'Equity Curve', 'Cash Curve', 'EMA Slopes'),
        row_heights=[0.5, 0.2, 0.15, 0.15]  # Adjust the relative heights of each subplot
    )

    # Plot price data (first subplot)
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines', name='Close Price', line=dict(color='dodgerblue')), row=1, col=1)

    # Plot EMAs (first subplot)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_50'], mode='lines', name='EMA 50', line=dict(color='yellow')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_200'], mode='lines', name='EMA 200', line=dict(color='lightblue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_1000'], mode='lines', name='EMA 200', line=dict(color='pink')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_5000'], mode='lines', name='EMA 200', line=dict(color='yellow')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_20000'], mode='lines', name='EMA 200', line=dict(color='red')), row=1, col=1)

    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_20_high'], mode='lines', name='EMA 200', line=dict(color='lightgreen')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_10_low'], mode='lines', name='EMA 200', line=dict(color='purple')), row=1, col=1)


    # Plot Ichimoku Cloud Base and Conversion Line (first subplot)
    fig.add_trace(go.Scatter(x=df['date'], y=df['ichimoku_base_line'], mode='lines', name='Ichimoku Base Line', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['ichimoku_conversion_line'], mode='lines', name='Ichimoku Conversion Line', line=dict(color='blue')), row=1, col=1)

    # Ichimoku Cloud - Green when Span A > Span B, Red when Span B > Span A
    # Senkou Span A (Green, Thicker Line)
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['ichimoku_a'],
        mode='lines', name='Senkou Span A',
        line=dict(color='green', width=3),  # Thicker line for Senkou Span A
        showlegend=True,  # Toggle on/off from legend
    ), row=1, col=1)

    # Senkou Span B (Red, Thicker Line)
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['ichimoku_b'],
        mode='lines', name='Senkou Span B',
        line=dict(color='red', width=3),  # Thicker line for Senkou Span B
        showlegend=True,  # Toggle on/off from legend
    ), row=1, col=1)

    # Add transparent grey fill between Senkou Span A and B
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['ichimoku_a'],
        mode='lines', line=dict(color='rgba(0,0,0,0)'),  # Invisible line for fill
        showlegend=False
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['ichimoku_b'],
        mode='lines', name='Ichimoku Cloud Fill',
        fill='tonexty', fillcolor='rgba(200, 200, 200, 0.1)',  # Lighter transparent grey fill
        showlegend=True,  # Toggle on/off from legend
    ), row=1, col=1)

    # Detect crossings between Senkou Span A and Span B (cloud change points)
    cloud_change_points = df[(df['ichimoku_a'] > df['ichimoku_b']) != (df['ichimoku_a'].shift(1) > df['ichimoku_b'].shift(1))]

    # Create single x and y arrays for green and red vertical lines
    green_lines_x = []
    green_lines_y = []
    red_lines_x = []
    red_lines_y = []

    # Add vertical lines on cloud change points
    for index, row in cloud_change_points.iterrows():
        if row['ichimoku_a'] > row['ichimoku_b']:  # Green line if Senkou Span A > Senkou Span B
            green_lines_x += [row['date'], row['date'], None]  # Adding None to break the line between changes
            green_lines_y += [min(df['close']), max(df['close']), None]
        else:  # Red line if Senkou Span B > Senkou Span A
            red_lines_x += [row['date'], row['date'], None]
            red_lines_y += [min(df['close']), max(df['close']), None]

    # Add a single trace for all green vertical lines
    fig.add_trace(go.Scatter(
        x=green_lines_x,
        y=green_lines_y,
        mode='lines',
        name='Cloud Change (Green)',  # Single legend entry for green lines
        line=dict(color='green', width=2),
        showlegend=True
    ))

    # Add a single trace for all red vertical lines
    fig.add_trace(go.Scatter(
        x=red_lines_x,
        y=red_lines_y,
        mode='lines',
        name='Cloud Change (Red)',  # Single legend entry for red lines
        line=dict(color='red', width=2),
        showlegend=True
    ))

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
        height=1200, width=1200, title_text='Backtest Results with Cloud and Colorful Vertical Lines', 
        showlegend=True, template='plotly_dark',
    )
    
    # Ensure that all subplots share the same x-axis type (categorical)
    fig.update_xaxes(type='category')

    # Show plot
    fig.show()

# Example usage: assuming df, buy_signals, sell_signals, and cash_equity_df are defined
# plot_backtest(df, buy_signals, sell_signals, cash_equity_df)
