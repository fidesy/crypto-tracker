from dotenv import load_dotenv
import json
import os
import psycopg2

load_dotenv()


def load_json(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        return json.load(f)


def insert_currencies():
    with psycopg2.connect(os.getenv("DBURL")) as connection:
        connection.autocommit = True
        cursor = connection.cursor()

        currencies = load_json("crypto_tracker/data/currencies.json")
        for currency in currencies:
            cursor.execute("INSERT INTO currencies(name, symbol, image_url) VALUES(%s, %s, %s)",
                (currency["name"], currency["symbol"], currency["image_url"]))


if __name__ == "__main__":
    insert_currencies()