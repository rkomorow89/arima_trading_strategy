import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import os
from datetime import datetime


def create_backtest_visualization(data, stats, bt):
    """
    Create comprehensive visualizations of the backtesting results
    """
    # Create plots directory if it doesn't exist
    plots_dir = "plots"
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Price chart with buy/sell signals
    ax1.plot(data.index, data['Close'], 'b-', linewidth=1, label='SPY Close Price', alpha=0.7)
    
    # Get trades from backtest
    if hasattr(bt, '_results') and hasattr(bt._results, '_trades'):
        trades = bt._results._trades
        if not trades.empty:
            # Plot buy signals
            buy_trades = trades[trades['Size'] > 0]
            if not buy_trades.empty:
                ax1.scatter(buy_trades['EntryTime'], buy_trades['EntryPrice'], 
                           color='green', marker='^', s=100, label='Buy Signals', zorder=5)
            
            # Plot sell signals
            sell_trades = trades[trades['Size'] < 0]
            if not sell_trades.empty:
                ax1.scatter(sell_trades['EntryTime'], sell_trades['EntryPrice'], 
                           color='red', marker='v', s=100, label='Sell Signals', zorder=5)
    
    ax1.set_title('SPY Price with ARIMA Trading Signals', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Price ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    # 2. Portfolio equity curve
    equity_curve = pd.Series(index=data.index, dtype=float)
    equity_curve.iloc[0] = 10000  # Starting cash
    
    # Simple equity curve calculation
    returns = data['Close'].pct_change().fillna(0)
    cumulative_returns = (1 + returns).cumprod()
    equity_curve = 10000 * cumulative_returns / cumulative_returns.iloc[0]
    
    ax2.plot(equity_curve.index, equity_curve.values, 'g-', linewidth=2, label='Portfolio Value')
    ax2.axhline(y=10000, color='gray', linestyle='--', alpha=0.7, label='Initial Capital')
    ax2.set_title('Portfolio Equity Curve', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Portfolio Value ($)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    # 3. Returns distribution
    returns_pct = data['Close'].pct_change().dropna() * 100
    ax3.hist(returns_pct, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    ax3.axvline(returns_pct.mean(), color='red', linestyle='--', linewidth=2, 
                label=f'Mean: {returns_pct.mean():.3f}%')
    ax3.set_title('Daily Returns Distribution', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Daily Return (%)')
    ax3.set_ylabel('Frequency')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Performance metrics summary
    ax4.axis('off')
    
    # Create performance summary text
    perf_text = f"""
    ARIMA Trading Strategy Performance Summary
    
    Key Metrics:
    • Total Return: {stats['Return [%]']:.2f}%
    • Sharpe Ratio: {stats.get('Sharpe Ratio', 'N/A'):.3f}
    • Max Drawdown: {stats.get('Max. Drawdown [%]', 'N/A'):.2f}%
    • Number of Trades: {stats.get('# Trades', 'N/A')}
    • Win Rate: {stats.get('Win Rate [%]', 'N/A'):.2f}%
    
    Strategy Details:
    • Period: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}
    • Data Points: {len(data)}
    • Initial Capital: $10,000
    • Commission: 0.1%
    
    ARIMA Model:
    • Uses confidence intervals for signals
    • Long when price < lower bound
    • Short when price > upper bound
    • Close position when in range
    """
    
    ax4.text(0.05, 0.95, perf_text, transform=ax4.transAxes, fontsize=11,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
    
    # Adjust layout and show
    plt.tight_layout()
    plt.suptitle('ARIMA Trading Strategy - Backtesting Results', fontsize=16, fontweight='bold', y=0.98)
    plt.subplots_adjust(top=0.93)
    
    # Save the plot
    filename = f"{plots_dir}/arima_backtest_results_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Backtest results saved to: {filename}")
    
    plt.show()
    
    # Create a separate detailed price chart for recent period
    create_recent_price_chart(data)
    
    # Create a summary report
    create_summary_report(data, stats)
    
    print("Visualizations created successfully!")


def create_recent_price_chart(data, months=6):
    """
    Create a detailed price chart for the recent period with moving averages
    
    Parameters:
    -----------
    data : pandas.DataFrame
        OHLC data with DatetimeIndex
    months : int, optional
        Number of months to show (default: 6)
    """
    # Create plots directory if it doesn't exist
    plots_dir = "plots"
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    
    # Show last X months for detail (approximately 22 trading days per month)
    days_to_show = months * 22
    recent_data = data.tail(days_to_show)
    
    ax.plot(recent_data.index, recent_data['Close'], 'b-', linewidth=2, label='SPY Close Price')
    
    # Add moving averages for context
    ma_20 = recent_data['Close'].rolling(window=20).mean()
    ma_50 = recent_data['Close'].rolling(window=50).mean()
    ax.plot(recent_data.index, ma_20, 'orange', linewidth=1.5, alpha=0.8, label='20-day MA')
    ax.plot(recent_data.index, ma_50, 'red', linewidth=1.5, alpha=0.8, label='50-day MA')
    
    ax.set_title(f'SPY Recent Price Action (Last ~{months} Months)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price ($)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    # Save the plot
    filename = f"{plots_dir}/spy_recent_price_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Recent price chart saved to: {filename}")
    
    plt.show()


def create_dual_plot(data, forecast, lo, hi):
    """
    Create a visualization with two subplots:
    - Upper plot: Complete price history
    - Lower plot: Last 30 days + ARIMA forecast
    
    Parameters:
    -----------
    data : pandas.Series
        Historical price data with DatetimeIndex
    forecast : pandas.Series or array-like
        ARIMA forecast values
    lo : array-like
        Lower confidence interval boundary
    hi : array-like
        Upper confidence interval boundary
    """
    print("\nCreating price data visualization...")
    
    # Create plots directory if it doesn't exist
    plots_dir = "plots"
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Upper plot: Complete price history
    ax1.plot(data.index, data.values, 'b-', linewidth=1.5, label='Complete SPY Price History')
    ax1.set_title('SPY Complete Price History', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Price ($)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    
    # Lower plot: Last 30 days + forecast
    last_30_days = data.tail(30)
    ax2.plot(last_30_days.index, last_30_days.values, 'b-', linewidth=2, label='Historical Prices (last 30 days)')
    
    # Prepare forecast data
    last_date = data.index[-1]
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=len(forecast), freq='D')
    
    # Plot forecast
    ax2.plot(forecast_dates, forecast, 'r--', linewidth=2, label='ARIMA Forecast', marker='o')
    
    # Confidence interval
    ax2.fill_between(forecast_dates, lo, hi, alpha=0.3, color='red', label='95% Confidence Interval')
    
    # Explicitly limit x-axis to 30 days + forecast
    start_date = last_30_days.index[0]
    end_date = forecast_dates[-1]
    ax2.set_xlim(start_date, end_date)
    
    ax2.set_title('SPY Price History - Last 30 Days + 5-Day Forecast', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Price ($)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Format x-axis for both plots
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot
    filename = f"{plots_dir}/arima_forecast_dual_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Dual forecast plot saved to: {filename}")
    
    # Show plot
    plt.show()
    
def create_single_forecast_plot(data, forecast, lo, hi, days_history=30):
    """
    Create a simple visualization with historical data and forecast
    
    Parameters:
    -----------
    data : pandas.Series
        Historical price data with DatetimeIndex
    forecast : pandas.Series or array-like
        ARIMA forecast values
    lo : array-like
        Lower confidence interval boundary
    hi : array-like
        Upper confidence interval boundary
    days_history : int, optional
        Number of historical days to display (default: 30)
    """
    # Create plots directory if it doesn't exist
    plots_dir = "plots"
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    plt.figure(figsize=(12, 6))
    
    # Historical data
    historical_data = data.tail(days_history)
    plt.plot(historical_data.index, historical_data.values, 'b-', linewidth=2, 
             label=f'Historical Prices (last {days_history} days)')
    
    # Prepare forecast data
    last_date = data.index[-1]
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=len(forecast), freq='D')
    
    # Plot forecast
    plt.plot(forecast_dates, forecast, 'r--', linewidth=2, label='ARIMA Forecast', marker='o')
    
    # Confidence interval
    plt.fill_between(forecast_dates, lo, hi, alpha=0.3, color='red', label='95% Confidence Interval')
    
    plt.title(f'SPY Price History - Last {days_history} Days + {len(forecast)}-Day Forecast', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.xticks(rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot
    filename = f"{plots_dir}/arima_forecast_single_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Single forecast plot saved to: {filename}")
    
    # Show plot
    plt.show()


def create_summary_report(data, stats, filename_suffix=""):
    """
    Create a comprehensive summary report with all key metrics and save to file
    
    Parameters:
    -----------
    data : pandas.DataFrame
        OHLC data
    stats : dict
        Backtesting statistics
    filename_suffix : str, optional
        Additional suffix for filename
    """
    # Create plots directory if it doesn't exist
    plots_dir = "plots"
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create summary text
    summary_text = f"""
ARIMA Trading Strategy - Backtesting Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
==================================================

STRATEGY PERFORMANCE METRICS:
• Total Return: {stats.get('Return [%]', 'N/A'):.2f}%
• Sharpe Ratio: {stats.get('Sharpe Ratio', 'N/A'):.3f}
• Max Drawdown: {stats.get('Max. Drawdown [%]', 'N/A'):.2f}%
• Volatility (Ann.): {stats.get('Volatility (Ann.) [%]', 'N/A'):.2f}%
• Number of Trades: {stats.get('# Trades', 'N/A')}
• Win Rate: {stats.get('Win Rate [%]', 'N/A'):.2f}%
• Best Trade: {stats.get('Best Trade [%]', 'N/A'):.2f}%
• Worst Trade: {stats.get('Worst Trade [%]', 'N/A'):.2f}%

DATA INFORMATION:
• Period: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}
• Total Data Points: {len(data)}
• Initial Capital: $10,000
• Commission: 0.1%

STRATEGY DESCRIPTION:
The ARIMA trading strategy uses autoregressive integrated moving average models
to generate price forecasts with confidence intervals. Trading signals are generated
based on current price position relative to forecast confidence bands:
- BUY signal when price < lower confidence bound
- SELL signal when price > upper confidence bound  
- CLOSE position when price within confidence range

RISK DISCLAIMER:
This backtesting analysis is for educational purposes only and does not constitute
investment advice. Past performance does not guarantee future results.
    """
    
    # Save to text file
    filename = f"{plots_dir}/arima_backtest_report_{timestamp}{filename_suffix}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(summary_text)
    
    print(f"Summary report saved to: {filename}")
    return filename
