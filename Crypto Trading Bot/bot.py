import json
import os.path
import sys
from datetime import *
import time
import numpy as np
import pandas as pd
from binance.client import Client
from decouple import config

client = Client(config("API_KEY"), config("SECRET_KEY"), testnet=True)  # Remove testnet for live trading
asset = "SOLEUR"
balance = client.get_asset_balance(asset=asset)
entryCutoff = 22.78
exitCutoff = 82.6667

def fetchKLines(asset):
    klines = client.get_historical_klines(asset, Client.KLINE_INTERVAL_1MINUTE, "1 hour ago UTC")
    klines = [[x[0], float(x[4])] for x in klines]
    klines = pd.DataFrame(klines, columns=["time", "price"])
    klines["time"] = pd.to_datetime(klines["time"], unit="ms")
    return klines

def log(message):
    print(f"LOG: {message}")
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    now = datetime.now()
    today = now.strftime("%d-%m-%Y")
    now = now.strftime("%H:%M:%S")
    with open(f"logs/{today}.txt", "a+") as logFile:
        logFile.write(f"{now} : {message}\n")

def calculate_rsi(data, window=14):  # RSI Calculation without pandas_ta
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def getRSI(asset):
    kLines = fetchKLines(asset)
    kLines["rsi"] = calculate_rsi(kLines["price"])  # Use custom RSI function
    return kLines['rsi'].iloc[-1]  # Return the latest RSI value

def createAccount():
    account = {
        "is_buying": True,
        "assets": {}
    }
    with open("botAccount.json", 'w') as f:
        f.write(json.dumps(account))
        f.close()

def do_trade(account, client, asset, side, quantity):
    if side == "buy":
        order = client.order_market_buy(symbol=asset, quantity=quantity)
        account["is_buying"] = False
    elif side == "sell":
        order = client.order_market_sell(symbol=asset, quantity=quantity)
        account["is_buying"] = True

    orderID = order["orderId"]
    print("Checking if order is filled")
    while order["status"] != "FILLED":
        order = client.get_order( symbol=asset, orderId=orderID)
        time.sleep(1)
        print("not yet")
        ### Maybe after 30 seconds of no luck, we cancel?
    print(order)
    price_paid = sum(float(fill["price"]) * float(fill["qty"]) for fill in order["fills"])
    logTrade(asset, side, price_paid, quantity)
    with open("botAccount.json", 'w') as f:
        f.write(json.dumps(account))

def logTrade(symbol, side, price, amount):
    print(f"TRADE COMPLETED: {side, price, amount}")
    if not os.path.isdir("trades"):
        os.mkdir("trades")
    now = datetime.now()
    today = now.strftime("%d-%m-%Y")
    now = now.strftime("%H:%M:%S")
    if not os.path.isfile(f"trades/{today}.csv"):
        with open(f"trades/{today}.csv", "w") as tradeFile:
                tradeFile.write("symbol,side,amount,price\n")
    with open(f"trades/{today}.csv", "a+") as tradeFile:
        tradeFile.write(f"{symbol},{side},{amount},{price}\n")




rsi = getRSI(asset)  # Get the initial RSI value
previousRSI = rsi

print("Trading time!")
while True:  # Infinite loop for trading logic
    try:
        if not os.path.exists("botAccount.json"):
            createAccount()

        with open("botAccount.json", 'r') as f:
            accountJson = json.load(f)

        print(accountJson)

        # Trading Logic
        previousRSI = rsi
        rsi = getRSI(asset)
        if accountJson["is_buying"]:
            if rsi < entryCutoff and previousRSI > entryCutoff:
                do_trade(accountJson, client, asset, side="buy", quantity=0.1)
        else:
            if rsi > exitCutoff and previousRSI < exitCutoff:
                do_trade(accountJson, client, asset, side="buy", quantity=0.1)
        print("current RSI: " + str(rsi))
        time.sleep(4)

    except Exception as e:
        log("ERROR:" + str(e))
        sys.exit()  # Exit on error
        pass  # Log error here

