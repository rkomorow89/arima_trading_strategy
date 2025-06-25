import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

from pmdarima import auto_arima
from backtesting import Backtest, Strategy
from utils import get_spy_data
from plotting import create_backtest_visualization

# ARIMA Trading Strategy Class
class ARIMAStrategy(Strategy):
    def init(self):
        # Fit ARIMA model on the full dataset
        print("Fitting ARIMA model for backtesting...")
        try:
            self.model = auto_arima(self.data.Close, seasonal=False, stepwise=True, 
                                  max_p=3, max_q=3, suppress_warnings=True)
            print(f"Best ARIMA model: {self.model.order}")
        except Exception as e:
            print(f"Error fitting ARIMA model: {e}")
            self.model = None
    
    def next(self):
        if self.model is None:
            return
            
        try:
            # Generate forecast
            forecast, conf_int = self.model.predict(n_periods=5, return_conf_int=True)
            lo, hi = conf_int[:,0].min(), conf_int[:,1].max()
            current_price = self.data.Close[-1]
            
            # Trading signals based on ARIMA confidence intervals
            if current_price < lo:  # Price below lower bound - go long
                if not self.position:
                    self.buy()
            elif current_price > hi:  # Price above upper bound - go short
                if not self.position:
                    self.sell()
            else:  # Price within range - close position
                if self.position:
                    self.position.close()
                    
        except Exception:
            # If forecast fails, do nothing
            pass

print("Starting ARIMA Backtesting Strategy...")

# 1. Load data with error handling using utils
data = get_spy_data(for_backtesting=True, date_range=("2020-01-01", "2025-06-24"))

if data is None or data.empty:
    print("Failed to obtain data. Exiting.")
    exit(1)

# Clean the data by removing any NaN values and interpolating missing values
print(f"Data shape before cleaning: {data.shape}")
print(f"NaN values before cleaning: {data.isnull().sum().sum()}")

# Fill any missing values and ensure no NaN values remain
data = data.ffill().bfill()
data = data.dropna()

# Ensure all OHLC relationships are maintained
data['High'] = data[['Open', 'High', 'Low', 'Close']].max(axis=1)
data['Low'] = data[['Open', 'High', 'Low', 'Close']].min(axis=1)

print(f"Data shape after cleaning: {data.shape}")
print(f"NaN values after cleaning: {data.isnull().sum().sum()}")

close = data['Close']
print(f"Successfully loaded {len(close)} data points from {close.index[0].date()} to {close.index[-1].date()}")
print(f"Price range: ${close.min():.2f} - ${close.max():.2f}")

# 2. Run backtest
print("Running backtest...")
try:
    bt = Backtest(data, ARIMAStrategy,
                  cash=10000, commission=.001,
                  hedging=True, exclusive_orders=True)
    stats = bt.run()
    print("\n=== Backtest Results ===")
    print(stats)
    
    # Additional performance metrics
    print("\n=== Additional Metrics ===")
    print(f"Total Return: {stats['Return [%]']:.2f}%")
    print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.3f}")
    print(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
    print(f"Number of Trades: {stats['# Trades']}")
    if stats['# Trades'] > 0:
        print(f"Win Rate: {stats['Win Rate [%]']:.2f}%")
    
    # 3. Create visualizations
    print("\nCreating visualizations...")
    create_backtest_visualization(data, stats, bt)
    
except Exception as e:
    print(f"Error running backtest: {e}")
    print("This might be due to insufficient data or model fitting issues.")
