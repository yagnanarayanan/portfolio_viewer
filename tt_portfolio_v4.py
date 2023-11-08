import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from requests import get
from pprint import PrettyPrinter
import os

# mention urls of all MFs from ticker tape
url_1 = "https://www.tickertape.in/mutualfunds/mirae-asset-large-cap-fund-M_MISL"
url_2 = "https://www.tickertape.in/mutualfunds/mirae-asset-midcap-fund-M_MIAI"
url_3 = "https://www.tickertape.in/mutualfunds/hdfc-small-cap-fund-M_HDFSU"
url_4 = "https://www.tickertape.in/mutualfunds/icici-pru-nasdaq-100-index-fund-M_ICIX1"
# make a list of these and iterate to fetch all current MF unit price
urls = [url_1, url_2, url_3, url_4]
mf_unit_prices = []
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title_string = soup.title.string
    pos = 0
    # find position of rupee symbol (numbers in the tile before the rupee symbol should not be considered)
    for char in title_string:
        if char == "₹":
            break
        pos += 1
    price = []
    for i in range(0, len(title_string)):
        # identify the unit price following position of rupee symbol
        if i > pos:
            if title_string[i].isdigit() or title_string[i] == ".":
                price.append(title_string[i])
    mf_1_price = float("".join(price))
    mf_unit_prices.append(mf_1_price)
# fetch the unit prices from a csv file where units of the MFs is present
unit_df = pd.read_csv("C:\\Users\\HP\\Desktop\\mf_units.csv", encoding='utf-8')
scheme_names = unit_df["Scheme Details"]
mf_unit_quantities_1 = unit_df["Units"]
mf_unit_quantities = []
for unit in mf_unit_quantities_1:
    mf_unit_quantities.append(unit)
total = 0
mf_individual_value = []
with open("portfolio_val_test.txt", "a", encoding="utf-8") as f:
    f.write(f"Portfolio as of {datetime.datetime.now()}:\n")
for i in range(0, 4):
    mf_val = mf_unit_quantities[i] * mf_unit_prices[i]
    mf_individual_value.append(mf_val)
    print(f"Mutual Fund {scheme_names[i]} valuation is ₹{mf_val}"
          f"for {mf_unit_quantities[i]}"
          f" quantity and unit price of ₹{mf_unit_prices[i]}")
    with open("portfolio_val_test.txt", "a", encoding="utf-8") as f:
        f.write(f"Mutual Fund {scheme_names[i]} valuation is ₹{mf_val} for {mf_unit_quantities[i]} quantity and unit "
                f"price of ₹{mf_unit_prices[i]}\n")
    total += mf_unit_quantities[i] * mf_unit_prices[i]
with open("portfolio_val_test.txt", "a", encoding="utf-8") as f:
    f.write(f"Total valuation is ₹{total} as of {datetime.datetime.now()}\n")
    f.write(
        f"Your large-cap holding is {round(((mf_individual_value[0] + mf_individual_value[3]) / total) * 100, 2)}% of total valuation\n")
    f.write(f"Your mid-cap holding is {round((mf_individual_value[1] / total) * 100, 2)}% of total valuation\n")
    f.write(f"Your small-cap holding is {round((mf_individual_value[2] / total) * 100, 2)}% of total valuation\n")
print(f"Total valuation is ₹{total} as of {datetime.datetime.now()}")
print(
    f"Your large-cap holding is {round(((mf_individual_value[0] + mf_individual_value[3]) / total) * 100, 2)}% of total "
    f"valuation")
print(f"Your mid-cap holding is {round((mf_individual_value[1] / total) * 100, 2)}% of total valuation")
print(f"Your small-cap holding is {round((mf_individual_value[2] / total) * 100, 2)}% of total valuation")
print("Consider re-balancing your portfolio, if required, for desired asset allocation.")
# currency converter
currency = input("Enter the currency in which you would like to convert this valuation: ")
printer = PrettyPrinter()
API_KEY = os.getenv("CURR_CONV_API_KEY")
BASE_URL = "https://free.currconv.com"
endpoint = f"/api/v7/convert?q=INR_{currency}&compact=ultra&apiKey={API_KEY}"
url = BASE_URL+endpoint
data = get(url).json()
rate = data[f"INR_{currency}"]
portfolio_valuation_in_alter_currency = float(rate) * total
print(f"Total valuation in alternate currency {currency} is {portfolio_valuation_in_alter_currency} at {rate} rate on"
      f" {datetime.datetime.now()}")
