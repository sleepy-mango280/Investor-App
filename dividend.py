import requests

API_KEY = 'kQ792Tix4ZyqVVGFslEG9pzNCd0wCMJ9'

print("Dividend Tracker (type 'done' when finished)\n")

portfolio = {}

# User inputs
while True:
    symbol = input("Enter stock symbol (or 'done' to finish): ").upper()
    if symbol == 'DONE':
        break
    try:
        shares = int(input(f"Enter number of shares for {symbol}: "))
        portfolio[symbol] = shares
    except ValueError:
        print(" Please enter a valid number of shares.")

# Fetch dividend info + calculate income
total_income = 0
print("\n Calculating dividend income...\n")

for symbol, shares in portfolio.items():
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data:
        dividend_per_share = data[0].get('lastDiv', 0)
        price = data[0].get('price', 1)
        dividend_yield = (dividend_per_share / price) if price else 0

        income = dividend_per_share * shares
        total_income += income

        print(f"{symbol}:")
        print(f"   Dividend Yield: {dividend_yield * 100:.2f}%")
        print(f"   Dividend/Share: ${dividend_per_share:.2f}")
        print(f"   Shares Owned: {shares}")
        print(f"   Annual Income: ${income:.2f}\n")
    else:
        print(f"{symbol}:  Data not found.\n")

# output
print(f" Total Annual Dividend Income: ${total_income:.2f}")
