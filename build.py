#!/usr/bin/python

import requests

r = requests.get(
    "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=ethereum-ecosystem&order=market_cap_desc&per_page=100&page=1&sparkline=false"
)
markets = r.json()
market_ids = [m["id"] for m in markets]
r = requests.get("https://api.coingecko.com/api/v3/coins/list?include_platform=true")
raw_contracts = r.json()


contracts = [
    {"symbol": coin["symbol"], "contract": coin["platforms"]["ethereum"]}
    for coin in raw_contracts
    if "ethereum" in coin["platforms"]
    and coin["id"] in market_ids
    and coin["platforms"]["ethereum"] != ""
]

import csv

with open("output/popular-erc20.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["name", "address"])
    for contract in contracts:
        writer.writerow([f"{contract['symbol'].upper()} Token", contract["contract"]])
