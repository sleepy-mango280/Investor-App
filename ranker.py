import requests

API_KEY = 'kQ792Tix4ZyqVVGFslEG9pzNCd0wCMJ9'

symbol = input("enter stock symbol:").upper()

# URLs for data
ratios_url = f'https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={API_KEY}'

# Request data
ratios_response = requests.get(ratios_url)

# Convert to JSON
ratios_data = ratios_response.json()

# Check if data is valid
if not ratios_data or isinstance(ratios_data, dict):
    print(f"Error: Unable to fetch data for {symbol}")
    exit()

# Retrieve P/E ratio
try:
    pe_ratio = ratios_data[0]['peRatioTTM']
    print("P/E ratio:", pe_ratio)
except (KeyError, IndexError, TypeError):
    pe_ratio = None
    print("P/E ratio not available.")

# Retrieve ROE (Return on Equity) - using correct field name for Financial Modeling Prep
try:
    roe = ratios_data[0]['returnOnEquityTTM']
    if roe is not None:
        print(f"ROE: {roe*100:.2f}%")
    else:
        roe = None
        print("ROE not available.")
except (KeyError, IndexError, TypeError):
    roe = None
    print("ROE not available.")

# Retrieve D/E ratio (Debt-to-Equity)
try:
    de_ratio = ratios_data[0]['debtEquityRatioTTM']
    if de_ratio is not None:
        print(f"D/E Ratio: {de_ratio:.2f}")
    else:
        de_ratio = None
        print("D/E Ratio not available.")
except (KeyError, IndexError, TypeError):
    de_ratio = None
    print("D/E Ratio not available.")

# P/E Ratio ranking
if pe_ratio is not None:
    if pe_ratio < 15:
        pe_score = 10
    elif pe_ratio < 25:
        pe_score = 8
    elif pe_ratio < 35:
        pe_score = 6
    else:
        pe_score = 4
else:
    pe_score = 0  # Default score if P/E is not available
print(f"P/E Score: {pe_score}/10")

# ROE scoring (higher is better, but check D/E ratio for extremely high ROE)
if roe is not None:
    if roe > 0.50:  # Above 50% - check if it's due to high debt
        if de_ratio is not None and de_ratio > 2.0:  # Very high debt (D/E > 2.0)
            roe_score = 3
            roe_warning = " (Warning: High ROE with very high debt - significant leverage risk)"
        elif de_ratio is not None and de_ratio > 1.0:  # Moderate high debt (D/E > 1.0)
            roe_score = 8
            roe_warning = " (Caution: High ROE with moderate debt levels)"
        else:
            # High ROE without excessive debt - excellent performance
            roe_score = 10
            roe_warning = " (Excellent: High ROE with manageable debt)"
    elif roe > 0.20:  # 20-50%
        roe_score = 10
        roe_warning = ""
    elif roe > 0.15:  # 15-20%
        roe_score = 8
        roe_warning = ""
    elif roe > 0.10:  # 10-15%
        roe_score = 6
        roe_warning = ""
    elif roe > 0:  # Positive ROE
        roe_score = 4
        roe_warning = ""
    else:
        roe_score = 0
        roe_warning = ""
else:
    roe_score = 0  # Default score if ROE is not available
    roe_warning = ""

print(f"ROE Score: {roe_score}/10{roe_warning}")

# Overall score calculation
if roe is not None and pe_ratio is not None:
    # Both metrics available - equal weight
    overall_score = (pe_score + roe_score) / 2
elif pe_ratio is not None and roe is None:
    # Only P/E available - use P/E with slight penalty
    overall_score = pe_score * 0.9  # 10% penalty for missing ROE
elif roe is not None and pe_ratio is None:
    # Only ROE available - use ROE with slight penalty
    overall_score = roe_score * 0.9  # 10% penalty for missing P/E
else:
    # No metrics available
    overall_score = 0

print(f"{symbol} is ranked: {overall_score:.1f}/10")
