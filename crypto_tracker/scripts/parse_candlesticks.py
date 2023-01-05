from datetime import datetime
from dotenv import load_dotenv
import os
import psycopg2
import requests


def parse_candlesticks():
    with psycopg2.connect(os.getenv("DBURL")) as connection:
        connection.autocommit = True
        cursor = connection.cursor()
        symbols = get_symbols(cursor)

        for symbol in symbols:
            candlesticks = get_candlesticks(symbol, "1d", 200)
            save_candlesticks(cursor, candlesticks)


def get_symbols(cursor):
    cursor.execute("SELECT symbol FROM currencies")
    symbols = cursor.fetchall()
    return [s[0] for s in symbols]


def get_candlesticks(symbol: str, interval: str, limit: int):
    symbol = symbol.upper()
    resp = requests.get(f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}")
    candlesticks = []
    res = resp.json()
    for r in res:
        candlesticks.append([datetime.fromtimestamp(r[6]/1000), symbol.lower(), *r[1:6]])

    return candlesticks

def save_candlesticks(cursor, candlesticks):
    cursor.executemany("""INSERT INTO candlesticks(date, symbol, open, high, low, close, volume) 
                            VALUES(%s, %s, %s, %s, %s, %s, %s)""", candlesticks)


if __name__ == "__main__":
    load_dotenv()
    parse_candlesticks()