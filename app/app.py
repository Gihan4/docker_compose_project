from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'gihanroey'
app.config['MYSQL_PASSWORD'] = 'roro123'
app.config['MYSQL_DB'] = 'db_prices'

mysql = MySQL(app)


@app.route("/")
def home_page():
    return render_template("HomePage.html")


@app.route("/eth")
def eth():
    # Make a GET request to the CoinStats API
    eth_response = requests.get("https://api.coinstats.app/public/v1/coins/ethereum")

    # Extract the Ethereum price from the API response
    if eth_response.status_code == 200:
        eth_price = eth_response.json()["coin"]["price"]

        # Insert the Ethereum price into the prices table
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "INSERT INTO prices (cryptocurrency, price) VALUES (%s, %s)"
        cursor.execute(query, ('Ethereum', eth_price))
        conn.commit()
        cursor.close()
        conn.close()

    # Pass the Ethereum price data to the template
    return render_template("eth.html", eth_price=eth_price)


@app.route("/btc")
def btc():
    # Make a GET request to the CoinDesk API
    btc_response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")

    # Extract the Bitcoin price from the API response
    if btc_response.status_code == 200:
        bitcoin_price = btc_response.json()["bpi"]["USD"]["rate"]

        # Insert the Bitcoin price into the prices table
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "INSERT INTO prices (cryptocurrency, price) VALUES (%s, %s)"
        cursor.execute(query, ('Bitcoin', bitcoin_price))
        conn.commit()
        cursor.close()
        conn.close()

    # Pass the Bitcoin price data to the template
    return render_template("btc.html", bitcoin_price=bitcoin_price)


@app.route("/get_prices")
def get_prices():
    # Retrieve all prices from the prices table
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT * FROM prices"
    cursor.execute(query)
    prices = cursor.fetchall()
    cursor.close()
    conn.close()

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
