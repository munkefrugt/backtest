import pandas as pd
import numpy as np
from trade import Trade
from plot_backtest import plot_backtest
from filter import filter_data_by_date_range, filter_data_by_ema_slope
from extra_indicators import add_extra_indicators #calculate_ema_slopes, get_more_ichimoku_indicators, get_extra_donchian, get_ema
from stats import buy_and_hold_compare_equity, update_streak, get_stats
from ichimoku_4H import process_and_merge_ichimoku
from ichimoku_15m import process_and_merge_ichimoku_15min

class BacktestSimulator:
    def __init__(self, initial_cash):
        self.previous_dc_20_high = None
        self.previous_dc_10_low = None
        self.previous_dc_100_high = None
        self.previous_dc_100_low = None
        self.previous_dc_500_low = None

        self.previous_ema_50_slope = None
        self.previous_ema_200_slope = None

        self.previous_ema_50 = None
        self.previous_ema_200 = None
        self.previous_ema_500 = None

        self.previous_ema_1000 = None

        self.previous_ema_5000 = None
        self.previous_ema_20000 = None

        self.previous_chikou_past = None
        self.previous_senkou_a_future = None
        self.previous_senkou_b_future = None

        self.cash = initial_cash
        self.equity = initial_cash
        self.trades = []
        self.buy_signals = []
        self.sell_signals = []
        self.cash_equity_records = []
        self.profits = []
        self.percentage_gains = []  # Store percentage gains here
        self.drawdowns = []
        self.current_drawdown = 0
        self.max_equity = initial_cash
        self.winning_streak = 0
        self.losing_streak = 0
        self.max_winning_streak = 0
        self.max_losing_streak = 0
        self.current_streak_type = None

        self.previous_close = None




        # 4 Hour 
        self.previous_chikou_past_4H  = None
        self.previous_past_cloud_top_4H  = None

        self.uptrend_4H = False
        self.dc_sell_zone = False
        self.uptrend = False
        # Store the crossover points (time and price)
        self.trend_start_4H = []  
        self.trend_end_4H = []  

    def run_backtest(self, df):
        df['break_up_marker'] = None
        df['break_down_marker'] = None
        df['equity'] = self.cash
        df['chikou_above_cloud_3_bars'] = df['chikou_26_past'] > df[['senkou_a_26_past', 'senkou_b_26_past']].max(axis=1)
        df['chikou_above_cloud_3_bars'] = df['chikou_above_cloud_3_bars'].rolling(window=3).sum() == 3

        for index, row in df.iterrows():
            self.row_simulator(row, index, df)  # Pass index correctly
        return df, pd.DataFrame(self.cash_equity_records, columns=['date', 'cash', 'equity', 'position'])

    def calculate_position_size(self, equity, cash, current_price, stop_loss, risk_percentage=0.02):
        risk_amount = equity * risk_percentage
        risk_per_share = current_price - stop_loss
        if risk_per_share != 0 :
            position_size_risk = risk_amount / risk_per_share

            position_size_cash = cash / current_price
            final_position_size = min(position_size_risk, position_size_cash)
        else : final_position_size = 0
        return final_position_size

    def row_simulator(self, row, current_index, df):
        current_time = row['date']
        current_price = row['close']
        dc_20_high = row['Donchian_20_high']
        dc_10_low = row['Donchian_10_low']
        dc_100_high = row['Donchian_100_high']
        dc_200_high = row['Donchian_200_high']

        dc_100_low = row['Donchian_100_low']
        dc_500_low = row['Donchian_500_low']


        ema_9 = row['EMA_9']
        ema_21 = row['EMA_21']
        ema_50 = row['EMA_50']
        ema_100 = row['EMA_100']
        ema_200 = row['EMA_200']
        ema_300 = row['EMA_300']
        ema_500 = row['EMA_500']

        #meta ema
        meta_ema_slope_200_ema_200 = row['meta_ema_slope_200_ema_200']


        ema_1000 = row['EMA_1000']
        ema_2000 = row['EMA_2000']
        ema_5000 = row['EMA_5000']
        ema_20000 = row['EMA_20000']
        
        ema_50_slope = row['EMA_50_slope']
        ema_200_slope = row['EMA_200_slope']
        ema_1000_slope = row['EMA_1000_slope']
        ema_5000_slope = row['EMA_5000_slope']

        kama_short = row['KAMA_short']
        kama_medium = row['KAMA_medium']
        kama_long = row['KAMA_long']
        kama_extra_long = row['KAMA_extra_long']

        equity = self.cash


        symbol = "SPX-USD"


        # ichimoku 1 minute: 


        tenkan_sen = row['ichimoku_conversion_line']
        kijun_sen = row['ichimoku_base_line']
        chikou_past = row['chikou_26_past']
        senkou_a = row['ichimoku_a']
        senkou_b = row['ichimoku_b']
        senkou_a_future = row['senkou_a_future']
        senkou_b_future = row['senkou_b_future']
        cloud_top = max(senkou_a, senkou_b)  # This is the cloud top

        # 15minute ichimoku: 
        senkou_a_15min = row['senkou_a_15min'] 
        senkou_b_15min = row['senkou_b_15min'] 
        chikou_span_15min  = row['chikou_span_15min'] 
        kijun_sen_15min = row['kijun_sen_15min'] 
        tenkan_sen_15min = row['tenkan_sen_15min'] 
        senkou_a_15min_future = row['senkou_a_15min_future']
        senkou_b_15min_future = row['senkou_a_15min_future']
        chikou_26_past_15min = row['chikou_26_past_15min']
        close_15min = row['close_15min'] #(same as chikou_26_past_15min)
        senkou_a_26_past_15min = row['senkou_a_26_past_15min'] 
        senkou_b_26_past_15min = row['senkou_b_26_past_15min']

        cloud_top_15min = max(senkou_a_15min, senkou_b_15min)  # This is the cloud top


        # 4 hour ichimoku timeframe:

        senkou_a_4H = row['senkou_a_4H'] 
        senkou_b_4H = row['senkou_b_4H'] 
        chikou_span_4H  = row['chikou_span_4H'] 
        kijun_sen_4H = row['kijun_sen_4H'] 
        tenkan_sen_4H = row['tenkan_sen_4H'] 
        senkou_a_4H_future = row['senkou_a_4H_future']
        senkou_b_4H_future = row['senkou_a_4H_future']
        chikou_26_past_4H = row['chikou_26_past_4H']
        close_4H = row['close_4H'] #(same as chikou_26_past_4H)
        senkou_a_26_past_4H = row['senkou_a_26_past_4H']
        senkou_b_26_past_4H = row['senkou_b_26_past_4H']
        already_in_trade = any(trade.status == 'open' for trade in self.trades)
        cloud_top_4H = max(senkou_a_4H, senkou_b_4H)  # This is the cloud top
        past_cloud_top_4H = max(senkou_a_26_past_4H, senkou_b_26_past_4H)

        #Equity
        equity = self.cash

        # check for the major uptrend. 
        # Check if the chikou breaks through the past cloud top (Break Up)
        # if chikou_26_past_4H > past_cloud_top_4H and (self.previous_chikou_past_4H is not None and self.previous_chikou_past_4H <= past_cloud_top_4H):
            
        #     df.at[current_index, 'break_up_marker'] = chikou_26_past_4H  # Mark the break-up point
        #     print(f'Break Up through past cloud at {current_time}, price: {chikou_26_past_4H}')
        #     self.uptrend_4H = True
        #     self.trend_start_4H.append((current_time, chikou_26_past_4H))




        # # 4H trend start
        #if (close_4H > past_cloud_top_4H) and
        if self.uptrend_4H == False: 
            if kijun_sen_4H > senkou_b_4H or kijun_sen_4H > senkou_b_4H: 
                if close_4H > tenkan_sen_4H > kijun_sen_4H:
                #if (tenkan_sen_4H > cloud_top_4H):
                    #if (senkou_a_4H > senkou_b_4H):
                    #if self.previous_ema_5000 is not None:
                        #if (ema_5000 > self.previous_ema_5000):
                        #if (current_price > ema_50 > ema_200 > ema_1000 > ema_5000> ema_20000 ):
                    df.at[current_index, 'break_up_marker'] = close_4H  # Mark the break-up point
                    print(f'Break Up through past cloud at {current_time}, price: {close_4H}')
                    self.uptrend_4H = True
                    self.trend_start_4H.append((current_time, close_4H))

        # 4 Hour trend ends
        if self.uptrend_4H == True: 
            if kijun_sen_4H < cloud_top_4H:
                df.at[current_index, 'break_down_marker'] = close_4H  # Mark the break-down point
                print(f'Break Down through past cloud at {current_time}, price: {close_4H}')
                self.uptrend_4H = False
                self.trend_end_4H.append((current_time, close_4H))

        # small buy trend starts
        #if ema_1000_slope > 0.02 and ema_5000_slope> 0.005 and ema_200_slope > 0.02:
        if ema_1000> ema_500:
            if self.uptrend == False: 
                self.uptrend = True


        # small buy trend ends


        if ema_500 < ema_1000:
            if self.uptrend == True:
                self.uptrend = False


        for open_trade in self.trades:
            if open_trade.status == 'open': 
                value_of_position = open_trade.position_size * current_price
                equity += value_of_position

        

        if self.previous_dc_20_high is not None and not already_in_trade:
            # Define a list of conditions (as lambdas)
            buy_conditions = [
                #LARGE FILTER
                # in use:
                #lambda: self.uptrend_4H,

                #lambda: self.uptrend,

                #lambda: chikou_26_past_4H > past_cloud_top_4H,
                #check chikou:
                #lambda: chikou_26_past_4H > past_cloud_top_4H and self.previous_chikou_past_4H < self.previous_past_cloud_top_4H,
                #lambda: current_price > past_cloud_top_4H
                #lambda: current_price > past_cloud_top_4H and self.previous_close < self.previous_past_cloud_top_4H,

                #lambda: current_price > cloud_top_4H,
                #lambda: ema_200 > ema_1000 >ema_5000 > ema_20000,

                
                #experiments
                #lambda: ema_200 > ema_1000 and self.previous_ema_200 < self.previous_ema_1000,
                #lambda: current_price > tenkan_sen_4H > kijun_sen_4H > cloud_top_4H,
                #lambda: ema_200_slope > 0,

                #medium



                #SMALL
                # lambda: row['chikou_3_days'] > current_price,  # Uncomment if needed
                #lambda: ema_50 > ema_200,  # EMA 50 > EMA 200
                #lambda: current_price > self.previous_dc_20_high,  # Breakout above Donchian 20 High
                #lambda: chikou_past > row['close_26_past'] and chikou_past > max(senkou_a, senkou_b),  # Chikou above cloud
                #lambda: ema_50_slope > ema_200_slope and self.previous_ema_50_slope < self.previous_ema_200_slope,  # EMA 50 slope greater than EMA 200
                #lambda: current_price > self.previous_dc_20_high,
                #lambda: self.previous_ema_50_slope < self.previous_ema_200_slope,

                # 
                # in use:
                #lambda: current_price > cloud_top,
                #lambda: ema_1000_slope > 0.02 and ema_5000_slope> 0.005 and ema_200_slope > 0.02,
                
                #lambda: ema_20 > ema_50> ema_100> ema_200 > ema_300>ema_500>ema_1000>ema_5000,
                #lambda: current_price > self.previous_dc_20_high,    
                #lambda: ema_1000_slope > 0.02,

                #ichimoku:
                
                #lambda: baseline >cloud_top,
                #lambda: senkou_a_future > senkou_b_future,
                #future cloud growing
                #lambda: senkou_a_future > self.previous_senkou_a_future,
                
                
                #lambda: current_price > self.previous_dc_500_high,
                #lambda: kama_short > kama_medium > kama_long > kama_extra_long,

                # det er det vi kører med. 

                #cross
                #note ema_1000 is higher than ema 200 and 300 the cross is happening below ema1000
                #lambda: ema_200 > ema_500 and self.previous_ema_200 < self.previous_ema_500,
                #lambda: ema_2000 >ema_1000 > ema_200 > ema_500, 
                #general up trend
                #lambda: ema_1000 > ema_5000 > ema_20000,
                #lambda: current_price > self.previous_dc_20_high,
 
                # få den gode pris: 
                #lambda: current_price circka ligmed kama_medium,


                # chat gpt strategy. buy at ema 9 /21 cross over
                #lambda: ema_9 > ema_21 and self.previous_ema_9 < self.previous_ema_21,
                #lambda: ema_200 > ema_500 > ema_2000 > ema_5000, 
                #lambda: current_price > self.previous_dc_100_high,

                # ichimoku 15min
                lambda: close_15min > tenkan_sen_15min > kijun_sen_15min> cloud_top_15min,
                lambda: current_price >ema_5000, 
                # ichimoku
                #lambda: kijun_sen > cloud_top ,
                #lambda: current_price > tenkan_sen > kijun_sen,
                lambda: current_price > cloud_top_4H ,

                
                ]
            
            # Check if all buy conditions are met
            if all(cond() for cond in buy_conditions):
                stop_loss = cloud_top_15min
                if stop_loss > current_price:   
                    stop_loss = current_price
                position_size = self.calculate_position_size(equity, self.cash, current_price, stop_loss)
                trade_id = len(self.trades) + 1
                trade = Trade(trade_id, symbol, current_price, stop_loss, current_price + (current_price - stop_loss) * 1.5, position_size, current_time)
                value_of_position = position_size * current_price
                self.cash -= value_of_position
                self.trades.append(trade)
                self.buy_signals.append((current_time, current_price))
                print("time of trade")
                print(current_time)


        # check if close has crossed into the sell zone.  

                
            
                    
        for trade in self.trades:
            if trade.status == 'open':
                #if self.previous_dc_500_low is not None:
                #    if current_price < self.previous_dc_500_low: #and self.uptrend: 
                #        self.dc_sell_zone = True
                    
                #if (self.dc_sell_zone == True) and (current_price >= ema_200) or : #or current_price < ema_1000:
                #if ema 200 crosses down and ema 100 is negative sloped
                #if ema_200 < ema_1000 and self.previous_ema_200 > self.previous_ema_1000 and ema_1000_slope < -0.001:
                #if current_price < self.previous_dc_500_low: #and current_price == kama_medium:
                if  kijun_sen_15min < cloud_top_15min:
                    self.sell(trade, current_time, current_price)
                    print("sell")
                    self.uptrend = False
                    self.dc_sell_zone = False

        self.previous_close = current_price
        self.previous_dc_20_high = dc_20_high
        self.previous_ema_9 = ema_9
        self.previous_ema_21 = ema_21

        self.previous_ema_200 = ema_200
        self.previous_ema_500 = ema_500
        self.previous_ema_1000 = ema_1000
        self.previous_ema_5000 = ema_5000
        self.previous_ema_20000 = ema_20000
        self.previous_chikou_past = chikou_past
        self.previous_dc_10_low = dc_10_low
        self.previous_dc_100_low = dc_100_low
        self.previous_dc_500_low = dc_500_low

        self.previous_dc_100_high = dc_100_high
        self.previous_dc_200_high = dc_200_high


        self.previous_ema_50_slope = ema_50_slope
        self.previous_ema_200_slope = ema_200_slope
        self.previous_senkou_a_future = senkou_a_future
        self.previous_senkou_b_future = senkou_b_future
        self.previous_chikou_past_4H = chikou_26_past_4H
        self.previous_past_cloud_top_4H = past_cloud_top_4H


        
        self.cash_equity_records.append([current_time, self.cash, equity, 0])

    def sell(self, trade, current_time, current_price):
        trade.close_trade(current_time, current_price)
        self.sell_signals.append((current_time, current_price))
        value_of_position = trade.position_size * current_price
        self.cash += value_of_position
        trade.status = 'closed'
        profit = value_of_position - (trade.position_size * trade.buy_price)
        
        # Calculate percentage gain or loss
        percentage_gain = ((current_price - trade.buy_price) / trade.buy_price) * 100
        self.percentage_gains.append(percentage_gain)

        self.profits.append(profit)
        update_streak(self, profit)
        print(f'Profit: {profit}, Percentage Gain: {percentage_gain:.2f}%')
        


# Load the data
path = '/home/martin/Documents/backtest/data/SPX_USD_2010_18_minute_ichimoku_EMA_DC_copy.csv'
df = pd.read_csv(path, low_memory=False)
#change name to date
df = df.rename(columns={"datetime": "date"})

# Run the function to process and merge 4-hour Ichimoku cloud data
df = process_and_merge_ichimoku(df, 'date')
df = process_and_merge_ichimoku_15min(df, 'date' )
# Filter data by date range
df = filter_data_by_date_range(df, start_year=2011, start_month=10, months=2)

#df = filter_data_by_date_range(df, start_year=2014, start_month=10, months=1)
# Print the times where the chikou 4H crossover occurred (without NaN values)



#df = df.tail(200)
#df = df.head(3000)
#df = df.tail(20000)

#df = get_more_ichimoku_indicators(df)
#df = get_ema(df)
# Calculate slopes for EMAs and acceleration
#df = calculate_ema_slopes(df)
#df = get_extra_donchian(df)
df = add_extra_indicators(df)

#df = filter_data_by_ema_slope(df)
# Run backtest
simulator = BacktestSimulator(initial_cash=1000)
df, cash_equity_df = simulator.run_backtest(df)


# Get and print stats
stats = get_stats(simulator, cash_equity_df)  # Pass the simulator object to the function
print(stats)

# Compare with buy-and-hold strategy
buy_and_hold_compare_equity(df, cash_equity_df)


# Plot the backtest results, including the slopes and acceleration
plot_backtest(df, simulator.buy_signals, simulator.sell_signals, cash_equity_df,simulator)