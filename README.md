
![gif](https://gist.github.com/dumbmoron/ea9b6264e6b6183fd590e322d1afab51/raw/bc064a9116403eab89e5b8200b1aa0890419ec0e/cat.gif)

# EUR/SOL Quantitative Trading Algorithm

This repository contains a quantitative trading algorithm built to trade the EUR/SOL currency pair using the BitStamp API and Binance Spot TestNet. The algorithm applies various trading strategies, including **RSI-based entry and exit points**, to optimize performance and minimize risks. Through backtesting and continuous refinement, the algorithm has been optimized to achieve higher returns with minimal overfitting.
## Features

- **Real-Time Trading**: Executes real-time trades on the EUR/SOL pair using the Binance Spot TestNet.
- **RSI Strategy**: Utilizes the **Relative Strength Index (RSI)** to define entry and exit points for trades.
- **Backtesting**: Uses **VectorBT** to allow users to backtest multiple strategies and visualize their respective performances.
- **Data Fetching**: Retrieves historical data via the BitStamp API for backtesting and strategy refinement.
- **Heatmap Performance**: Visualizes strategy performance across multiple thresholds for optimal strategy selection.
- **Logging & Monitoring**: Saves trade execution & any error details to separate logs, allowing for debugging if needed.
## Installation

If you'd like to, you can install this project 

```bash
  git clone https://github.com/BaileyC03/EurSOL-Trading-Bot.git
  cd EurSOL-Trading-Bot

```

Just make sure to install all of the dependencies! 
```bash
    pip3 install numpy pandas python-binance python-decouple tqdm vectorbt
```
After this, you'll need to create an .env file with your binance keys. You can create them [here](https://testnet.binance.vision/):

``` bash
 API_KEY=whateverYourKeyIs
 SECRET_KEY=whateverYourSecretKeyIs
 ```

## Example Output:
This is how it ((should)) look, when working properly.
``` bash
Trade Completed: Buy at 22.78, Amount: 0.1
Current RSI: 55.23
```
