import requests

# Bitstamp API endpoint for getting market info
url = "https://www.bitstamp.net/api/v2/trading-pairs-info/"

# Make the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    pairs = [market['name'] for market in data]
    print("Available trading pairs:")
    for pair in pairs:
        print(pair)
else:
    print("Failed to retrieve data.")
