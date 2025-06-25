"""
Utility functions for data download and processing
"""

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def download_data_with_alpha_vantage(ticker, outputsize='full', api_key=None, date_range=None):
    """Download data using Alpha Vantage API with fallback to synthetic data"""
    if api_key is None:
        # Try to get API key from environment variable
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        if api_key and api_key != 'your_api_key_here':
            print("Using Alpha Vantage API key from .env file")
        else:
            # Fallback to demo key
            api_key = 'demo'
            print("No valid API key found in .env file. Using demo key (limited functionality).")
            print("Get your free API key from: https://www.alphavantage.co/support/#api-key")
            print("Add it to your .env file as: ALPHA_VANTAGE_API_KEY=your_actual_key")
    
    # Set default date range if not provided
    if date_range is None:
        date_range = ("2024-01-01", "2025-06-01")
    
    try:
        print(f"Downloading {ticker} data from Alpha Vantage...")
        ts = TimeSeries(key=api_key, output_format='pandas')
        
        # Get daily adjusted stock data
        data, meta_data = ts.get_daily_adjusted(symbol=ticker, outputsize=outputsize)
        
        if data.empty:
            print(f"No data received for {ticker} from Alpha Vantage.")
            return generate_synthetic_spy_data(date_range[0], date_range[1])
        
        # Alpha Vantage returns data in descending order, so we need to reverse it
        data = data.sort_index()
        
        # Filter to our desired date range
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        data = data[(data.index >= start_date) & (data.index <= end_date)]
        
        print(f"Successfully downloaded {len(data)} data points from Alpha Vantage")
        return data
        
    except Exception as e:
        print(f"Error downloading data from Alpha Vantage: {e}")
        print("Using synthetic data for demonstration...")
        return generate_synthetic_spy_data(date_range[0], date_range[1])

def download_data_with_yfinance(ticker, date_range=None):
    """Download data using yfinance - free and reliable"""
    # Set default date range if not provided
    if date_range is None:
        date_range = ("2024-01-01", "2025-06-01")
    
    try:
        import yfinance as yf
        print(f"Downloading {ticker} data from Yahoo Finance...")
        
        # Download data
        stock = yf.Ticker(ticker)
        data = stock.history(start=date_range[0], end=date_range[1])
        
        if data.empty:
            print(f"No data received for {ticker} from Yahoo Finance.")
            return None
        
        print(f"Successfully downloaded {len(data)} data points from Yahoo Finance")
        return data
        
    except ImportError:
        print("yfinance not installed. Please install it with: pip install yfinance")
        return None
    except Exception as e:
        print(f"Error downloading data from Yahoo Finance: {e}")
        return None

def download_data_alternative_free_sources(ticker, date_range=None):
    """Alternative free data sources without API keys"""
    # Set default date range if not provided
    if date_range is None:
        date_range = ("2024-01-01", "2025-06-01")
    
    # Try yfinance first (most reliable free source)
    yf_data = download_data_with_yfinance(ticker, date_range)
    if yf_data is not None and not yf_data.empty:
        return yf_data
    
    try:
        # Try using pandas_datareader with FRED (Federal Reserve Economic Data)
        # This works for major indices like SP500
        import pandas_datareader as pdr
        
        if ticker.upper() == 'SPY':
            # For SPY, we can use S&P 500 data from FRED
            print("Trying to download S&P 500 data from FRED...")
            data = pdr.get_data_fred('SP500', start=date_range[0], end=date_range[1])
            if not data.empty:
                print(f"Successfully downloaded {len(data)} data points from FRED")
                # Convert to Series with proper name
                sp500_data = data.iloc[:, 0]  # Return the first column
                sp500_data.name = 'Close'
                return sp500_data
    except Exception as e:
        print(f"Alternative data source failed: {e}")
    
    return None

def generate_synthetic_spy_data(start, end, for_backtesting=False):
    """Generate synthetic SPY-like data for demonstration purposes"""
    print("Generating synthetic SPY data for demonstration...")
    date_range = pd.date_range(start=start, end=end, freq='D')
    # Remove weekends
    date_range = date_range[date_range.weekday < 5]
    
    # Start with a base price around SPY's typical range
    np.random.seed(42)  # For reproducible results
    base_price = 450
    returns = np.random.normal(0.0005, 0.015, len(date_range))  # Daily returns with realistic volatility
    
    # Generate price series with some trending behavior
    prices = [base_price]
    trend = 0.0002  # Small upward trend
    for i, ret in enumerate(returns[1:]):
        # Add some trending behavior
        trend_component = trend * (i / len(returns))
        prices.append(prices[-1] * (1 + ret + trend_component))
    
    close_prices = np.array(prices)
    
    if for_backtesting:
        # Create OHLC data for backtesting
        open_prices = close_prices * (1 + np.random.normal(0, 0.002, len(close_prices)))
        high_prices = np.maximum(open_prices, close_prices) * (1 + np.abs(np.random.normal(0, 0.008, len(close_prices))))
        low_prices = np.minimum(open_prices, close_prices) * (1 - np.abs(np.random.normal(0, 0.008, len(close_prices))))
        volumes = np.random.randint(50000000, 200000000, len(close_prices))
        
        data = pd.DataFrame({
            'Open': open_prices,
            'High': high_prices,
            'Low': low_prices,
            'Close': close_prices,
            'Volume': volumes
        }, index=date_range[:len(close_prices)])
        
        return data
    else:
        # Return only close prices for ARIMA modeling
        return pd.Series(close_prices, index=date_range[:len(close_prices)])

def prepare_data_for_backtesting(data):
    """Convert data to OHLC format required for backtesting"""
    if isinstance(data, pd.Series):
        # If we only have close prices, create synthetic OHLC data
        close_data = data.dropna()  # Remove any NaN values first
        
        # Generate realistic OHLC data based on close prices
        np.random.seed(42)  # For reproducible results
        daily_volatility = 0.02  # 2% typical daily volatility
        
        # Calculate daily returns to estimate realistic spreads
        returns = close_data.pct_change().fillna(0)
        volatility = returns.rolling(window=20, min_periods=1).std().fillna(daily_volatility)
        
        # Generate OHLC with realistic relationships
        spread_factor = volatility * 0.5  # Half the volatility for intraday spread
        
        open_data = close_data.shift(1).fillna(close_data.iloc[0])  # Previous close as open
        open_data = open_data + (close_data - open_data) * np.random.uniform(0.1, 0.9, len(close_data))
        
        high_data = np.maximum(open_data, close_data) * (1 + np.abs(np.random.normal(0, spread_factor, len(close_data))))
        low_data = np.minimum(open_data, close_data) * (1 - np.abs(np.random.normal(0, spread_factor, len(close_data))))
        
        # Ensure proper OHLC relationships
        high_data = np.maximum(high_data, np.maximum(open_data, close_data))
        low_data = np.minimum(low_data, np.minimum(open_data, close_data))
        
        # Generate realistic volume based on price movements
        price_change = np.abs(returns)
        base_volume = 100000000  # 100M average volume
        volume_data = base_volume * (1 + price_change * 5)  # Higher volume on big moves
        
        result_data = pd.DataFrame({
            'Open': open_data,
            'High': high_data,
            'Low': low_data,
            'Close': close_data,
            'Volume': volume_data.astype(int)
        }, index=close_data.index)
        
        # Final cleanup to ensure no NaN values
        result_data = result_data.ffill().bfill().dropna()
        
        return result_data
    
    elif isinstance(data, pd.DataFrame):
        # Check if it's already in the right format
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if all(col in data.columns for col in required_columns):
            # Clean existing OHLC data
            clean_data = data[required_columns].copy()
            clean_data = clean_data.ffill().bfill().dropna()
            return clean_data
        
        # If it's Alpha Vantage format, convert it
        if '5. adjusted close' in data.columns:
            result_data = pd.DataFrame({
                'Open': data['1. open'],
                'High': data['2. high'], 
                'Low': data['3. low'],
                'Close': data['5. adjusted close'],
                'Volume': data['6. volume']
            })
            result_data = result_data.ffill().bfill().dropna()
            return result_data
    
    # If we can't handle the format, raise an error
    raise ValueError(f"Cannot convert data format to OHLC. Data type: {type(data)}, Columns: {data.columns if hasattr(data, 'columns') else 'N/A'}")

def get_spy_data(for_backtesting=False, date_range=None):
    """
    Main function to get SPY data with multiple fallback options
    
    Args:
        for_backtesting (bool): If True, returns OHLC data suitable for backtesting
        date_range (tuple): (start_date, end_date) as strings
    
    Returns:
        pandas.DataFrame or pandas.Series: SPY data
    """
    # Set default date range
    if date_range is None:
        if for_backtesting:
            date_range = ("2020-01-01", "2025-06-01")
        else:
            date_range = ("2024-01-01", "2025-06-01")
    
    print(f"Starting data download for SPY (backtesting: {for_backtesting})...")
    data = None
    
    # Try free alternatives first (yfinance is much more reliable)
    print("Trying free data sources...")
    alt_data = download_data_alternative_free_sources("SPY", date_range=date_range)
    if alt_data is not None and not alt_data.empty:
        data = alt_data
        print("Successfully obtained data from free sources!")
    
    # Only try Alpha Vantage as a fallback if free sources fail
    if data is None or data.empty:
        print("Free sources failed, trying Alpha Vantage...")
        data = download_data_with_alpha_vantage("SPY", date_range=date_range)
    
    # If all else fails, use synthetic data
    if data is None or data.empty:
        print("All data sources failed. Using synthetic data...")
        data = generate_synthetic_spy_data(date_range[0], date_range[1], for_backtesting=for_backtesting)
    
    # Prepare data for backtesting if needed
    if for_backtesting:
        if not isinstance(data, pd.DataFrame) or not all(col in data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']):
            data = prepare_data_for_backtesting(data)
    else:
        # For ARIMA modeling, we only need close prices
        if isinstance(data, pd.DataFrame):
            if '5. adjusted close' in data.columns:
                data = data['5. adjusted close']
            elif 'Close' in data.columns:
                data = data['Close']
            else:
                # Take the first column if we can't identify close price
                data = data.iloc[:, 0]
    
    return data
