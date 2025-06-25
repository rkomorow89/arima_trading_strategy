import warnings
from pmdarima import auto_arima
from utils import get_spy_data
from plotting import create_dual_plot
from datetime import datetime, timedelta

# Suppress future warnings and statsmodels warnings to clean up output
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='No supported index is available')
warnings.filterwarnings('ignore', category=UserWarning, module='statsmodels')

# Download SPY data with error handling
print("Starting ARIMA modeling for SPY...")

# Calculate yesterday's date
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# Use the utility function to get SPY data for ARIMA modeling
data = get_spy_data(for_backtesting=False, date_range=("2024-01-01", yesterday))

if data is None or len(data) == 0:
    print("Failed to obtain data. Exiting.")
    exit(1)

# Remove missing values (important for FRED and other sources)
data = data.dropna()

print(f"Successfully loaded {len(data)} data points from {data.index[0].date()} to {data.index[-1].date()}")
print(f"Price range: ${data.min():.2f} - ${data.max():.2f}")



# Fit ARIMA model
print("Fitting ARIMA model...")
try:
    model = auto_arima(data, seasonal=False, stepwise=True,
                       information_criterion="bic", max_p=3, max_q=3,
                       suppress_warnings=True)
    print(f"Best ARIMA model: {model.order}")
    
    # Generate forecast
    forecast, conf_int = model.predict(n_periods=5, return_conf_int=True)
    lo, hi = conf_int[:,0], conf_int[:,1]
    
    print("\n=== ARIMA Forecast Results ===")
    current_date = data.index[-1].strftime('%Y-%m-%d')
    print(f"Current price ({current_date}): ${data.iloc[-1]:.2f}")
    print("Forecast horizon: 5 periods")
    print(f"Predicted range: ${lo.min():.2f} – ${hi.max():.2f}")
    print(f"Average forecast: ${forecast.mean():.2f}")
    
    # Show individual forecasts with dates
    print("\nDetailed 5-day forecast:")
    n = min(5, len(forecast), len(lo), len(hi))
    if n == 0:
        print("No forecast values available.")
    else:
        import pandas as pd
        last_date = data.index[-1]
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=n, freq='D')
        
        for i in range(n):
            # forecast is a Pandas Series, lo/hi are NumPy Arrays
            f_val = float(forecast.iloc[i])
            l_val = float(lo[i])
            h_val = float(hi[i])
            date_str = forecast_dates[i].strftime('%Y-%m-%d')
            print(f"Day {i+1} ({date_str}): ${f_val:.2f} (Range: ${l_val:.2f} - ${h_val:.2f})")
    
    # Visualization of price data with forecast
    create_dual_plot(data, forecast, lo, hi)
        
except Exception as e:
    print(f"Error fitting ARIMA model: {e}")
    print("This might be due to insufficient data or data quality issues.")
