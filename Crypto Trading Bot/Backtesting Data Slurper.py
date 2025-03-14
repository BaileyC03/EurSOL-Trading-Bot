import json
import pandas as pd
import requests
import datetime
from tqdm import tqdm  # Import tqdm for progress bar

currencyPair = "soleur"  # CHANGE THIS TO ANY PAIR YOU WANT
apiURL = f"https://www.bitstamp.net/api/v2/ohlc/{currencyPair}/"

startDate = "2024-08-01"
endDate = pd.Timestamp.today()

dates = pd.date_range(start=startDate, end=endDate, freq="3h")
dates = [int(item.timestamp()) for item in dates]

masterData = []

# Wrap the loop with tqdm for a progress bar
for first, last in tqdm(zip(dates, dates[1:]), total=len(dates) - 1, desc="Fetching Data"):
    params = {
        "step": 60,  # Time (seconds) between each data point
        "limit": 60,  # Number of data points to be saved
        "start": first,
        "end": last,
    }

    apiData = requests.get(apiURL, params=params)
    data = apiData.json().get("data", {}).get("ohlc", [])
    masterData.extend(data)  # More efficient than `masterData = masterData + data`

df = pd.DataFrame(masterData)
df["timestamp"] = df["timestamp"].astype(int)
print(df)

df.to_csv("dataforbacktesting.csv", index=False)
