# ARIMA Trading Strategy with Backtesting (Windows)

This project implements a complete ARIMA-based trading strategy for SPY (SPDR S&P 500 ETF) with automated backtesting and performance analysis. **Optimized for Windows systems.**

## ⚠️ IMPORTANT NOTE FOR WINDOWS USERS ⚠️

**Before you start:** Conda requires special handling on Windows:
- ALWAYS open a new PowerShell window as Administrator before working with conda
- After creating a new environment: Close PowerShell completely and open a new window
- Only then you can activate the environment

## Description

The project consists of two main components:

1. **ARIMA Modeling** (`arima_modeling.py`): Basic time series forecasting
2. **Trading Strategy with Backtesting** (`arima_backtesting.py`): Complete implementation of an ARIMA-based trading strategy

The strategy uses ARIMA confidence intervals for signal generation: Long positions when prices are below the predicted lower bound and short positions when prices are above the upper bound.

## Features

- **Automatic ARIMA Modeling**: Uses `auto_arima` for optimal parameter finding
- **Modular Visualization**: Separate `plotting.py` with reusable plot functions
- **Automatic Plot Saving**: All visualizations are automatically saved in the `plots/` subfolder
- **Dual-Plot Visualization**: Combined display of complete price history and detailed forecast
- **Reliable Data Source**: Default Yahoo Finance (via `yfinance`), with fallback to FRED (`pandas_datareader`) and Alpha Vantage
- **Multiple Data Sources**: `yfinance`, FRED (Federal Reserve, via `pandas_datareader`), Alpha Vantage, with fallback to synthetic data
- **Free APIs**: Works with free API keys
- **Trading Signals**: Based on ARIMA confidence intervals
- **Backtesting**: Complete performance analysis with the `backtesting` library
- **Comprehensive Visualizations**: Automatic creation and saving of:
  - Performance Dashboard (4-panel overview)
  - Detailed price charts with moving averages
  - Trading signal visualizations
  - Returns distribution analysis
- **Risk Management**: Configurable commissions and trading parameters
- **Performance Metrics**: Detailed statistics and key figures
- **Windows-optimized**: Special handling for Windows environments
- **Modular Structure**: Central utils.py for all data operations and plotting.py for visualizations
- **Secure API Configuration**: .env file for API keys
- **Dynamic Date Calculation**: Automatic adjustment to yesterday as data end date

## Installation (Windows)

**Prerequisites:**

- Windows 10/11
- Python 3.8 or higher
- PowerShell or Command Prompt

## 🚀 Quick Start for Windows Users

1. **Clone/download repository**
   ```powershell
   git clone <repository-url>
   cd arima
   ```
   
   *Or download and extract ZIP file*

2. **Create virtual environment (IMPORTANT: Use Python 3.11)**
   ```powershell
   # Use Python 3.11 (recommended for best compatibility)
   python3.11 -m venv venv
   # If python3.11 is not available:
   # py -3.11 -m venv venv
   
   .\venv\Scripts\Activate.ps1
   ```
   
   *If you have problems with PowerShell Execution Policy:*
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

   **⚠️ IMPORTANT**: Python 3.13 has compatibility issues with `pmdarima`. Use Python 3.11 for best results!

3. **Check Python version**
   ```powershell
   python --version
   # Should show Python 3.11.x
   ```

4. **Install packages**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Alternative: Conda Installation (Recommended for Windows)

Conda is often more stable on Windows:

**⚠️ IMPORTANT FOR WINDOWS USERS:**
1. ALWAYS open a new PowerShell window as Administrator before working with conda
2. After environment creation: Close PowerShell completely and open a new window!

```powershell
# 1. Download Miniconda: https://docs.conda.io/en/latest/miniconda.html
# 2. After installation: Close PowerShell completely and open new as Administrator!

# 3. Create conda environment (in a NEW PowerShell window as Admin)
conda create -n arima-env python=3.11

# 4. ⚠️ IMPORTANT: Close PowerShell completely and open NEW window!
# 5. Then activate:
conda activate arima-env

# 6. ✅ Check if environment is activated (should show "(arima-env)" in prompt)
conda info --envs

# Install main packages via Conda (backtesting not available)
conda install -c conda-forge pmdarima matplotlib pandas numpy scipy

# Install Alpha Vantage and Backtesting package separately via pip
pip install alpha-vantage backtesting pandas-datareader python-dotenv
```

**⚠️ Important Notes:**

- **ALWAYS open a new PowerShell window** before working with conda
- The `backtesting` and `alpha-vantage` packages are not available via conda-forge and must be installed via pip
- After `conda activate arima-env` no confirmation message appears - this is normal!
- You should see `(arima-env)` at the beginning of your PowerShell prompt
- If not visible: `conda info --envs` shows all available environments

### 🔑 Alpha Vantage API Key (Free)

**Important**: For best results, you should get a free Alpha Vantage API key:

1. Go to: https://www.alphavantage.co/support/#api-key
2. Register for free (only email required)
3. Copy your free API key
4. **Open the `.env` file in the project folder**
5. **Replace `your_api_key_here` with your actual API key:**
   ```env
   ALPHA_VANTAGE_API_KEY=YOUR_ACTUAL_API_KEY
   ```

**Free Limits**: 5 requests per minute, 500 per day - more than sufficient for this project!

**Security**: The `.env` file is automatically ignored by Git and not shared publicly.

## Usage

### 1. Simple ARIMA Modeling

Run the basic model:

```powershell
python arima_modeling.py
```

**Common Error:** `ModuleNotFoundError: No module named 'alpha_vantage'`
**Solution:** Install packages with: `pip install alpha-vantage pmdarima pandas numpy pandas-datareader`

**API Key**: The script works with the demo key, but for best results you should use a free API key from Alpha Vantage.

The script will:

- Use Alpha Vantage API (no rate-limiting issues like with Yahoo Finance)
- Fall back to FRED (Federal Reserve data) on API problems
- Generate synthetic SPY-like data if all APIs fail
- Fit an optimal ARIMA model
- Create a 5-period forecast
- Output the predicted price range

### 2. Trading Strategy with Backtesting

Run the complete trading strategy:

```powershell
python arima_backtesting.py
```

The backtesting strategy implements the following logic:

- **Data Range**: SPY data from 2020-01-01 to 2025-06-24
- **Model**: Automatic ARIMA (max_p=3, max_q=3, no seasonality)
- **Signal Generation**:
  - **Long Signal**: When current price is below the predicted lower bound
  - **Short Signal**: When current price is above the predicted upper bound
  - **Neutral**: When price is within the predicted range
- **Backtesting Parameters**:
  - Initial Capital: $10,000
  - Commission: 0.1% per trade
  - Hedging: Enabled
  - Exclusive Orders: Enabled

The backtesting outputs detailed performance statistics, including:

- Total return
- Sharpe Ratio
- Maximum Drawdown
- Number of trades
- Win rate
- Additional risk and performance metrics

## ⚠️ Troubleshooting

### Common Problems and Solutions

**1. Alpha Vantage API Problems**
```text
KeyError: 'Error Message'
```

- **Problem**: API key invalid or API limit reached
- **Solution**: Get free API key from https://www.alphavantage.co/support/#api-key
- **Fallback**: The script automatically switches to FRED or synthetic data

**2. No Internet Connection**

- **Problem**: No connection to external APIs possible
- **Solution**: The script automatically generates synthetic SPY-like data
- **Advantage**: Works offline for demonstration purposes

**3. Missing Packages**
```text
ModuleNotFoundError: No module named 'alpha_vantage'
```

- **Solution**: Install all required packages:
  ```powershell
  pip install alpha-vantage pmdarima pandas numpy pandas-datareader yfinance backtesting matplotlib scipy
  ```

**4. pmdarima Installation on Windows**
```
ERROR: Failed building wheel for pmdarima
```
- **Solution**: Use conda instead of pip:
  ```powershell
  conda install -c conda-forge pmdarima
  ```

**5. Sklearn Deprecation Warnings**
- **Problem**: Warnings about deprecated sklearn parameters
- **Impact**: Only warnings, functionality not affected
- **Solution**: Ignore these warnings - they are harmless

## Configuration

### ARIMA Modeling (`arima_modeling.py`)

The following parameters can be adjusted:

- **Ticker Symbol**: Default is "SPY", can be changed to other stocks/ETFs
- **Time Period**: Start and end date of historical data
- **Forecast Horizon**: Number of periods to predict (`n_periods`)
- **ARIMA Parameters**: `max_p`, `max_q`, `information_criterion`

### Backtesting (`arima_backtesting.py`)

Adjustable parameters:

- **Ticker Symbol**: Default is "SPY"
- **Time Period**: Date range for backtesting (currently: 2020-2025)
- **Initial Capital**: `cash` (Default: $10,000)
- **Commissions**: `commission` (Default: 0.1%)
- **ARIMA Parameters**: `max_p`, `max_q` (Default: 3 each)
- **Forecast Horizon**: `n_periods` for signal generation (Default: 5)

## Dependencies (Windows-optimized)

**For the basic ARIMA model (`arima_modeling.py`):**

- `yfinance`: Standard data source (Yahoo Finance, free and reliable)
- `pandas-datareader`: Fallback for FRED data (Federal Reserve)
- `alpha-vantage`: Additional fallback (API key recommended but not mandatory)
- `python-dotenv`: Loading environment variables from .env file
- `pmdarima`: Automatic ARIMA modeling (can be complex to install on Windows)
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical calculations
- `matplotlib`: Plotting and visualizations

**Additionally for backtesting (`arima_backtesting.py`):**

- `backtesting`: Backtesting framework for trading strategies
- `scipy`: Scientific calculations

**For visualizations (`plotting.py`):**

- `matplotlib`: Main library for all plots and charts
- `pandas`: For date and time series processing in plots

## Output

### ARIMA Modeling Output (`arima_modeling.py`)

The script shows detailed information about the entire process:

**With successful data transfer and modeling:**
```text
Starting ARIMA modeling for SPY...
Successfully loaded 357 data points from 2024-01-02 to 2025-06-24
Price range: $445.23 - $578.91
Fitting ARIMA model...
Best ARIMA model: (2, 1, 1)

=== ARIMA Forecast Results ===
Current price (2025-06-24): $565.43
Forecast horizon: 5 periods
Predicted range: $558.12 – $572.87
Average forecast: $565.49

Detailed 5-day forecast:
Day 1 (2025-06-25): $565.78 (Range: $558.12 - $573.44)
Day 2 (2025-06-26): $565.89 (Range: $556.77 - $575.01)
Day 3 (2025-06-27): $565.95 (Range: $555.34 - $576.56)
Day 4 (2025-06-28): $566.01 (Range: $553.89 - $578.13)
Day 5 (2025-06-29): $566.07 (Range: $552.42 - $579.72)

Creating price data visualization...
Dual forecast plot saved to: plots/arima_forecast_dual_20250625_185110.png
```

**New Visualization:**
The script now creates a two-stage visualization with English labels:
- **Upper Plot**: "SPY Complete Price History" - Complete SPY price history over the entire period
- **Lower Plot**: "SPY Price History - Last 30 Days + 5-Day Forecast" - Detail view of the last 30 days plus 5-day ARIMA forecast with confidence interval

**Automatic Saving:**
All plots are automatically saved in the `plots/` subfolder:
- `plots/arima_forecast_dual_YYYY-MM-DD_HHMMSS.png` - Main forecast visualization (Dual-Plot)
- The `plots/` folder is automatically created if it doesn't exist

**Plot Labels (English):**
- Titles: "SPY Complete Price History" and "SPY Price History - Last 30 Days + 5-Day Forecast"
- Legends: "Complete SPY Price History", "Historical Prices (last 30 days)", "ARIMA Forecast", "95% Confidence Interval"
- Axis labels: "Price ($)" and "Date"

**With API problems/fallback:**
```text
Starting ARIMA modeling for SPY...
Using demo API key. For production use, get your free API key from: https://www.alphavantage.co/support/#api-key
Downloading SPY data from Alpha Vantage...
Error downloading data from Alpha Vantage: API rate limit exceeded
Trying to download S&P 500 data from FRED...
Successfully downloaded 357 data points from FRED
...

Creating price data visualization...
Dual forecast plot saved to: plots/arima_forecast_dual_20250625_185110.png
```

The predicted range is based on the confidence intervals of the 5-period forecast.

### Backtesting Output (`arima_backtesting.py`)

The backtesting script outputs comprehensive performance statistics and automatically creates detailed visualizations, e.g.:

```text
Start                     2020-01-02 00:00:00
End                       2025-05-30 00:00:00
Duration                   1943 days 00:00:00
Exposure Time [%]                    85.23
Equity Final [$]                  12543.21
Equity Peak [$]                   13102.45
Return [%]                           25.43
Buy & Hold Return [%]                18.76
Return (Ann.) [%]                     4.67
Volatility (Ann.) [%]                12.34
Sharpe Ratio                         0.378
Sortino Ratio                        0.521
Calmar Ratio                         0.243
Max. Drawdown [%]                   -19.21
Avg. Drawdown [%]                    -3.45
Max. Drawdown Duration        156 days 00:00:00
Avg. Drawdown Duration         23 days 00:00:00
# Trades                               145
Win Rate [%]                         52.41
Best Trade [%]                        8.67
Worst Trade [%]                      -6.23
Avg. Trade [%]                        0.16
Max. Trade Duration            15 days 00:00:00
Avg. Trade Duration             5 days 00:00:00
Profit Factor                         1.23
Expectancy [%]                        0.21
SQN                                   0.84
```

**Automatic Visualizations:**
The backtesting creates and saves multiple visualizations automatically in the `plots/` folder:

1. **Performance Dashboard** (`arima_backtest_results_YYYY-MM-DD_HHMMSS.png`):
   - 4-panel overview with SPY price and trading signals
   - Portfolio equity curve
   - Returns distribution histogram
   - Performance metrics summary

2. **Detailed Price Charts** (`spy_recent_price_YYYY-MM-DD_HHMMSS.png`):
   - Last 6 months SPY price development
   - 20-day and 50-day moving averages
   - High-resolution display of current market situation

3. **Performance Report** (`arima_backtest_report_YYYY-MM-DD_HHMMSS.txt`):
   - Textual summary of all important metrics
   - Strategy parameters and time period
   - Suitable for documentation and reports

**Folder Structure:**
```
plots/
├── arima_forecast_dual_20250625_185110.png
├── arima_backtest_results_20250625_185004.png
├── spy_recent_price_20250625_185010.png
└── arima_backtest_report_20250625_185013.txt
```

## 📈 Plot Interpretation - Guide to Understanding the Visualizations

### 1. ARIMA Forecast Plots (arima_modeling.py)

#### Dual-Plot Visualization (`arima_forecast_dual_*.png`)

**Upper Plot - Complete Price History:**

- **Blue Line**: SPY price history over the entire analysis period
- **Plot Title**: "SPY Complete Price History"
- **Purpose**: Context for long-term trends and market phases
- **Interpretation**:
  - Upward trends show bull markets
  - Downward trends show bear markets
  - Sideways movements show consolidation phases
  - Volatility is recognizable through fluctuation range

**Lower Plot - Detailed Forecast:**

- **Blue Line**: Historical prices of the last 30 days (Label: "Historical Prices (last 30 days)")
- **Red dashed line with dots**: 5-day ARIMA forecast (Label: "ARIMA Forecast")
- **Red shading**: 95% confidence interval of the forecast (Label: "95% Confidence Interval")
- **Plot Title**: "SPY Price History - Last 30 Days + 5-Day Forecast"
- **Axis Labels**: Y-axis "Price ($)", X-axis "Date"

**Interpretation Aids:**

- **Narrow confidence intervals**: High model confidence, stable forecast
- **Wide confidence intervals**: Higher uncertainty, volatile market situation
- **Forecast above recent prices**: Model expects price increase
- **Forecast below recent prices**: Model expects price decline
- **Forecast trend**: Shows expected short-term direction

**Deriving Trading Signals:**

- Current price below lower confidence bound → Potential long signal
- Current price above upper confidence bound → Potential short signal
- Price within confidence interval → No clear signal

### 2. Backtesting Performance Dashboard (`arima_backtest_results_*.png`)

#### Panel 1: SPY Price with ARIMA Trading Signals (Top Left)

- **Plot Title**: "SPY Price with ARIMA Trading Signals"
- **Blue Line**: SPY price history over backtesting period (Label: "SPY Close Price")
- **Green Dots/Arrows**: Buy signals (Label: "Buy Signals")
- **Red Dots/Arrows**: Sell signals (Label: "Sell Signals")
- **Y-Axis**: "Price ($)"

**Interpretation:**

- **Signal Frequency**: Shows strategy activity
- **Signal Timing**: Quality of entry and exit points
- **Signal Clustering**: Areas with many signals = volatile market phases
- **Signal Quality**: Visual assessment whether signals occur at extremes

#### Panel 2: Portfolio Equity Curve (Top Right)

- **Plot Title**: "Portfolio Equity Curve"
- **Green Line**: Portfolio value over time (Label: "Portfolio Value")
- **Gray dashed line**: Initial capital (Label: "Initial Capital")
- **Y-Axis**: "Portfolio Value ($)"

**Interpretation:**

- **Rising trend**: Profitable strategy
- **Smooth curve**: Consistent performance
- **Volatile curve**: Risky performance
- **Drawdowns**: Loss phases (distance to previous high)
- **Final value vs. Buy & Hold**: Comparison to passive investment strategy

**Evaluation Criteria:**

- Equity curve above starting line = Profit
- Steady upward movement = Good strategy
- Large fluctuations = High volatility
- Long loss phases = High drawdowns

#### Panel 3: Daily Returns Distribution (Bottom Left)

- **Plot Title**: "Daily Returns Distribution"
- **Blue Histogram**: Distribution of daily returns
- **Red dashed line**: Average return (Label: "Mean: X.XXX%")
- **X-Axis**: "Daily Return (%)", **Y-Axis**: "Frequency"

**Interpretation:**

- **Normal distribution**: Healthy return distribution
- **Right skew**: More large gains than losses (positive)
- **Left skew**: More large losses than gains (negative)
- **Fat tails**: Extreme events more frequent than expected
- **Average near zero**: Low average daily return is normal
- **Wide distribution**: High volatility

#### Panel 4: Performance Metrics Summary (Bottom Right)

**Understanding Key Metrics:**

- **Total Return**: Total return over backtesting period
  - >0% = Profit, <0% = Loss
  - Comparison with Buy & Hold Return important

- **Sharpe Ratio**: Risk-adjusted return
  - >1.0 = Very good
  - 0.5-1.0 = Good
  - <0.5 = Weak
  - <0 = Losses

- **Max Drawdown**: Largest loss from peak
  - <-10% = Acceptable
  - -10% to -20% = Moderate
  - >-20% = High risk

- **Win Rate**: Percentage of profitable trades
  - >60% = Very good
  - 50-60% = Good
  - <50% = Weak (can be compensated by large gains)

### 3. Detailed Price Charts (`spy_recent_price_*.png`)

**Plot Information:**
- **Plot Title**: "SPY Recent Price Action (Last ~6 Months)"
- **X-Axis**: "Date", **Y-Axis**: "Price ($)"

**Main Elements:**

- **Blue Line**: SPY price history (last 6 months) - Label: "SPY Close Price"
- **Orange Line**: 20-day moving average - Label: "20-day MA"
- **Red Line**: 50-day moving average - Label: "50-day MA"

**Technical Analysis:**

- **Price above both MAs**: Upward trend
- **Price below both MAs**: Downward trend
- **MA crossovers**: Trend change signals
- **20-MA above 50-MA**: Bullish trend
- **20-MA below 50-MA**: Bearish trend

**Support and Resistance:**

- **MA lines as support**: Price bounces from below
- **MA lines as resistance**: Price bounces from above
- **Breakouts**: Confirmation of trend changes

### 4. Performance Reports (`arima_backtest_report_*.txt`)

**Important Sections:**

**Time Series Metrics:**

- **Start/End**: Backtesting period
- **Duration**: Total duration of analysis
- **Exposure Time**: Percent of time with open positions

**Return Metrics:**

- **Return [%]**: Absolute total return
- **Return (Ann.) [%]**: Annualized return
- **Buy & Hold Return**: Comparison return with buy-and-hold

**Risk Metrics:**

- **Volatility (Ann.)**: Annual fluctuation range
- **Max. Drawdown**: Largest loss
- **Calmar Ratio**: Return/Max-Drawdown ratio

**Trading Metrics:**

- **# Trades**: Number of trades
- **Avg. Trade Duration**: Average holding period
- **Profit Factor**: Ratio of gains/losses

### 5. Interpretation Checklist for Trading Decisions

**✅ Positive Signals:**

- Sharpe Ratio > 0.5
- Win Rate > 50%
- Profit Factor > 1.0
- Max Drawdown < -15%
- Rising equity curve
- Narrow confidence intervals

**⚠️ Warning Signals:**

- Sharpe Ratio < 0
- Win Rate < 45%
- Max Drawdown > -25%
- Many consecutive losses
- Very wide confidence intervals
- Sideways/falling equity curve

**📊 Evaluate Market Context:**

- Current market phase (Bull/Bear/Sideways)
- Volatility of recent weeks
- Position of MAs relative to price
- Proximity to historical highs/lows

### 6. Avoiding Common Interpretation Errors

**❌ Typical Mistakes:**

- Overweighting individual metrics
- Understanding confidence intervals as guarantees
- Seeing backtesting performance as future guarantee
- Underestimating drawdowns
- Ignoring transaction costs

**✅ Correct Approach:**

- Consider multiple metrics together
- Evaluate risk-return ratio
- Include market context
- Consider worst-case scenarios
- Plan regular model updates

## Advanced Usage

The project can be extended with:

- **Advanced Visualizations**: Additional plot types in `plotting.py` (residual analysis, correlograms)
- Model diagnostics and residual analysis
- Seasonal ARIMA models (SARIMA)
- Parameter optimization for the trading strategy
- Risk management features (stop-loss, take-profit)
- Multi-asset backtesting
- Walk-forward analysis
- Export of forecast results and backtesting reports
- **Interactive Plots**: Integration of Plotly for interactive visualizations
- **Custom Plot Functions**: Extension of `plotting.py` with additional analysis tools

## 📊 Visualizations and Plot Management

### Automatic Saving

All visualizations are automatically saved:

- **Folder**: `plots/` (automatically created)
- **Filenames**: Timestamped for unique identification
- **Formats**: High-resolution PNG files (300 DPI)
- **Reports**: Additional text files with performance summaries

### Plot Types

**ARIMA Modeling (`arima_modeling.py`):**

- Dual-plot with complete price history and forecast detail
- Single-forecast plot for simple display

**Backtesting (`arima_backtesting.py`):**

- 4-panel performance dashboard
- Detailed price charts with technical indicators
- Performance text reports

### Plot Organization

```
plots/
├── arima_forecast_dual_20250625_185110.png      # ARIMA Forecast (Dual-Plot)
├── arima_backtest_results_20250625_185004.png   # Backtesting Dashboard
├── spy_recent_price_20250625_185010.png         # Detailed Price Analysis
└── arima_backtest_report_20250625_185013.txt    # Performance Report
```

**All plots are saved in the same `plots/` folder with:**

- **Timestamp**: Format `YYYY-MM-DD_HHMMSS` for chronological sorting
- **Unique filenames**: Different analysis types are distinguishable by prefixes
- **Automatic creation**: The `plots/` folder is automatically created on first plot

**Advantages:**

- Complete traceability of all analyses
- Easy comparison of different time points
- Professional documentation for reports
- No manual saving operations required

## Strategy Description

The implemented ARIMA trading strategy is based on the mean-reversion hypothesis:

1. **Model Training**: An ARIMA model is fitted to historical SPY price data
2. **Forecast Creation**: The model creates 5-period forecasts with confidence intervals
3. **Signal Generation**:
   - **Long Position**: When current price is below the predicted lower bound (assumption: price will return to center)
   - **Short Position**: When current price is above the predicted upper bound (assumption: price will return to center)
   - **No Trade**: When price is within the predicted range

4. **Risk Management**: Commissions of 0.1% per trade simulate realistic trading costs

## File Overview

- `arima_modeling.py`: Basic ARIMA modeling and forecast creation (uses utils.py and plotting.py)
- `arima_backtesting.py`: Complete trading strategy with backtesting (uses utils.py and plotting.py)
- `plotting.py`: **Advanced Visualization Library** - All plot functions for ARIMA analyses
  - `create_dual_plot()` - Combined display: complete price history + detailed forecast
  - `create_single_forecast_plot()` - Simple forecast visualization (configurable)
  - `create_backtest_visualization()` - Comprehensive backtesting visualizations (4-panel dashboard)
  - `create_recent_price_chart()` - Detailed price charts with moving averages
  - **Automatic Saving**: All functions automatically save plots in the `plots/` folder
- `utils.py`: **Central File** - All data download functions and processing logic
  - `get_spy_data()` - Main function with automatic fallback options
  - `download_data_with_alpha_vantage()` - Alpha Vantage API integration with .env support
  - `download_data_alternative_free_sources()` - FRED as free alternative
  - `generate_synthetic_spy_data()` - Synthetic data generation
  - `prepare_data_for_backtesting()` - OHLC formatting for backtesting
- `requirements.txt`: List of all required Python packages (with Alpha Vantage and python-dotenv)
- `.env`: Configuration file for API keys (secure and not in Git)
- `.gitignore`: Git ignore file (protects .env from accidental publication)
- `plots/`: **Automatically created folder** for all saved visualizations
  - Contains timestamped PNG files and text reports
  - Automatically created on first plot
- `README_DE.md`: German documentation
- `README_EN.md`: English documentation

---
