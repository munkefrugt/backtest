import plotly.graph_objs as go
import plotly.subplots as sp
import pandas as pd

def plot_backtest(df, buy_signals, sell_signals, cash_equity_df, simulator):
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


    # first subplot
    
    #ichimoku 15m
    fig.add_trace(go.Scatter(x=df['date'], y=df['close_15min'], mode='lines', name='close_15min', line=dict(color='purple')), row=1, col=1)

    fig.add_trace(go.Scatter(x=df['date'], y=df['chikou_26_past_15min'], mode='lines', name='chikou_26_past_15min', line=dict(color='cyan')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['senkou_a_26_past_15min'], mode='lines', name='senkou_a_26_past_15min', line=dict(color='yellow')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['senkou_b_26_past_15min'], mode='lines', name='senkou_b_26_past_15min', line=dict(color='orange')), row=1, col=1)
    #4 Hour extended.    
    fig.add_trace(go.Scatter(x=df['date'], y=df['senkou_a_15min'], mode='lines', name='senkou_a_15min', line=dict(color='green')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['senkou_b_15min'], mode='lines', name='senkou_b_15min', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['chikou_span_15min'], mode='lines', name='chikou_span_15min', line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['kijun_sen_15min'], mode='lines', name='kijun_sen_15min', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['tenkan_sen_15min'], mode='lines', name='tenkan_sen_15min', line=dict(color='crimson')), row=1, col=1)


    #4 Hour     
    
    #fig.add_trace(go.Scatter(x=df['date'], y=df['real_close_as_chikou_4H'], mode='lines', name='real_close_as_chikou_4H', line=dict(color='orange')), row=1, col=1)

    #helper past 4 hour ichimoku remove?
    fig.add_trace(go.Scatter(x=df['date'], y=df['close_4H'], mode='lines', name='close_4H', line=dict(color='purple')), row=1, col=1)

    fig.add_trace(go.Scatter(x=df['date'], y=df['chikou_26_past_4H'], mode='lines', name='chikou_26_past_4H', line=dict(color='cyan')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['senkou_a_26_past_4H'], mode='lines', name='senkou_a_26_past_4H', line=dict(color='yellow')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['senkou_b_26_past_4H'], mode='lines', name='senkou_b_26_past_4H', line=dict(color='orange')), row=1, col=1)
    #4 Hour extended.    
    fig.add_trace(go.Scatter(x=df['date'], y=df['senkou_a_4H'], mode='lines', name='senkou_a_4H', line=dict(color='green')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['senkou_b_4H'], mode='lines', name='senkou_b_4H', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['chikou_span_4H'], mode='lines', name='chikou_span_4H', line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['kijun_sen_4H'], mode='lines', name='kijun_sen_4H', line=dict(color='crimson')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['tenkan_sen_4H'], mode='lines', name='tenkan_sen_4H', line=dict(color='blue')), row=1, col=1)

    # trend_start_4H
    fig.add_trace(go.Scatter(
        x=[crossover[0] for crossover in simulator.trend_start_4H], 
        y=[crossover[1] for crossover in simulator.trend_start_4H], 
        mode='markers', name='trend_start_4H', 
        marker=dict(color='orange', symbol='circle', size=20)
    ), row=1, col=1)

    
    # trend_end_4H
    fig.add_trace(go.Scatter(
        x=[crossover[0] for crossover in simulator.trend_end_4H], 
        y=[crossover[1] for crossover in simulator.trend_end_4H], 
        mode='markers', name='trend_end_4H', 
        marker=dict(color='blue', symbol='circle', size=20)
    ), row=1, col=1)


    #MINUTE TIMEFRAME
    #KAMA: 
    fig.add_trace(go.Scatter(x=df['date'], y=df['KAMA_short'], mode='lines', name='adaptive moving short', line=dict(color='green')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['KAMA_medium'], mode='lines', name='adaptive moving medium', line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['KAMA_long'], mode='lines', name='adaptive moving long', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['KAMA_extra_long'], mode='lines', name='adaptive moving extra long', line=dict(color='purple')), row=1, col=1)


    #EMA's
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_9'], mode='lines', name='EMA 9', line=dict(color='yellow')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_21'], mode='lines', name='EMA 21', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_50'], mode='lines', name='EMA 50', line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_100'], mode='lines', name='EMA 100', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_200'], mode='lines', name='EMA 200', line=dict(color='black')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_300'], mode='lines', name='EMA 300', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_500'], mode='lines', name='EMA 500', line=dict(color='purple')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_1000'], mode='lines', name='EMA 1000', line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_2000'], mode='lines', name='EMA 2000', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_5000'], mode='lines', name='EMA 5000', line=dict(color='yellow')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_20000'], mode='lines', name='EMA 20000', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_100000'], mode='lines', name='EMA 100000', line=dict(color='yellow')), row=1, col=1)

    #DC high
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_20_high'], mode='lines', name='DC_20_high', line=dict(color='green')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_100_high'], mode='lines', name='DC_100_high', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_200_high'], mode='lines', name='DC_200_high', line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_500_high'], mode='lines', name='DC_500_high', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_1000_high'], mode='lines', name='DC_1000_high', line=dict(color='purple')), row=1, col=1)
    #DC low
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_10_low'], mode='lines', name='DC 10 low', line=dict(color='purple')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_50_low'], mode='lines', name='DC 50 low', line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_100_low'], mode='lines', name='DC 100 low', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_200_low'], mode='lines', name='DC 200 low', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Donchian_500_low'], mode='lines', name='DC 500 low', line=dict(color='green')), row=1, col=1)
    
    # Plot price data (first subplot)
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines', name='Close Price', line=dict(color='grey')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['close_26_past'], mode='lines', name='close_26_past', line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['chikou_26_past'], mode='lines', name='chikou_26_past', line=dict(color='orange')), row=1, col=1)



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
    fig.add_trace(go.Scatter(x=cash_equity_df['date'], y=cash_equity_df['equity'], mode='lines', name='Equity Curve', line=dict(color='cyan')), row=2, col=1)

    # Plot cash curve (third subplot)
    fig.add_trace(go.Scatter(x=cash_equity_df['date'], y=cash_equity_df['cash'], mode='lines', name='Cash Curve', line=dict(color='yellow')), row=3, col=1)

    # Plot EMA slopes (fourth subplot)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_50_slope'], mode='lines', name='EMA 50 Slope', line=dict(color='yellow')), row=4, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_200_slope'], mode='lines', name='EMA 200 Slope', line=dict(color='lightblue')), row=4, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_1000_slope'], mode='lines', name='EMA 1000 Slope', line=dict(color='red')), row=4, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_5000_slope'], mode='lines', name='EMA 5000 Slope', line=dict(color='blue')), row=4, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['EMA_20000_slope'], mode='lines', name='EMA 20000 Slope', line=dict(color='green')), row=4, col=1)

    #slope Meta EMA

    fig.add_trace(go.Scatter(x=df['date'], y=df['meta_ema_slope_200_ema_50'], mode='lines', name='meta_ema_slope_200_ema_50', line=dict(color='red')), row=4, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['meta_ema_slope_200_ema_200'], mode='lines', name='meta_ema_slope_200_ema_200', line=dict(color='green')), row=4, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['meta_ema_slope_1000_ema_200'], mode='lines', name='meta_ema_slope_1000_ema_200', line=dict(color='blue')), row=4, col=1)

    # Update layout to make sure the x-axis is categorical and aligned across all subplots
    fig.update_layout(
        height=1200, width=1200, title_text='Backtest Results with Cloud and Colorful Vertical Lines', 
        showlegend=True,# template='plotly_dark',
    )
    
    # Ensure that all subplots share the same x-axis type (categorical)
    fig.update_xaxes(type='category')

    # Show plot
    fig.show()

