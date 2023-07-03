from flask import Flask, render_template, jsonify
import mysql.connector
import requests

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="db",
    user="gihanroey",
    password="roro123",
    database="db_prices"
)

mycursor = mydb.cursor()
print("connected")

@app.route("/")
def home_page():
    return render_template("HomePage.html")

@app.route("/eth")
def eth():
    eth_response = requests.get("https://api.coinstats.app/public/v1/coins/ethereum")

    if eth_response.status_code == 200:
        eth_price = eth_response.json()["coin"]["price"]

        # Insert the Ethereum price into the prices table
        query = "INSERT INTO prices (cryptocurrency, price) VALUES (%s, %s)"
        values = ('Ethereum', eth_price)
        mycursor.execute(query, values)
        mydb.commit()

    return render_template("eth.html", eth_price=eth_price)

@app.route("/btc")
def btc():
    btc_response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")

    if btc_response.status_code == 200:
        bitcoin_price = btc_response.json()["bpi"]["USD"]["rate"]

        # Insert the Bitcoin price into the prices table
        query = "INSERT INTO prices (cryptocurrency, price) VALUES (%s, %s)"
        values = ('Bitcoin', bitcoin_price)
        mycursor.execute(query, values)
        mydb.commit()

    return render_template("btc.html", bitcoin_price=bitcoin_price)

@app.route("/get_prices")
def get_prices():
    query = "SELECT * FROM prices"
    mycursor.execute(query)
    prices = mycursor.fetchall()

    # Prepare the price data as a list of dictionaries
    price_data = []
    for price in prices:
        price_data.append({
            'id': price[0],
            'cryptocurrency': price[1],
            'price': price[2],
            'timestamp': price[3]
        })

    # Return the price data as JSON
    return jsonify(price_data)

if __name__ == '__main__':
    app.run()
