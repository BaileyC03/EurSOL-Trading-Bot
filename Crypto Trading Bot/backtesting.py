import pandas as pd
import numpy as np
import vectorbt as vbt

interval = 10

metric = "total_return"

# Load the data from CSV file
pricing = pd.read_csv('dataforbacktesting.csv')[["timestamp", "close"]]

# Convert the 'timestamp' column to datetime format
pricing["date"] = pd.to_datetime(pricing["timestamp"], unit='s')
pricing.set_index("date", inplace=True)
pricing = pricing.asfreq('min')

# Calculate RSI (Relative Strength Index) using the 'close' column
rsi = vbt.RSI.run(pricing["close"], window=14, short_name="RSI")

# Define entry and exit points using RSI thresholds
entryPoints = np.linspace(1, 50, num=interval)  # Define entry points between 25 and 30
exitPoints = np.linspace(50, 99, num=interval)  # Define exit points between 80 and 85

# Create a 2D grid of entry and exit points
grid = np.array(np.meshgrid(entryPoints, exitPoints)).T.reshape(-1, 2)

# Generate entries and exits based on RSI crossing thresholds
entries = rsi.rsi_crossed_below(list(grid[:, 0]))  # Detect when RSI crosses below entry points
exits = rsi.rsi_crossed_above(list(grid[:, 1]))  # Detect when RSI crosses above exit points

# Create a portfolio using the generated entries and exits
portfolio = vbt.Portfolio.from_signals(pricing["close"], entries, exits)

# Retrieve and print portfolio performance based on the defined metric
portfolioPerformance = portfolio.deep_getattr(metric)

# Create a matrix for portfolio performance and print it
portfolioPerformanceMatrix = portfolioPerformance.vbt.unstack_to_df(index_levels="rsi_crossed_above",
                                                                    column_levels="rsi_crossed_below")

# Generate a heatmap of the portfolio performance matrix
portfolioPerformanceMatrix.vbt.heatmap(
    xaxis_title="entry",  # Label for the x-axis (entry points)
    yaxis_title="exit",  # Label for the y-axis (exit points)
).show()
print("done")
