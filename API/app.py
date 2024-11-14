import matplotlib
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os


from flask import Flask, jsonify, send_file
from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
matplotlib.use('Agg')

api_key = os.getenv("API_KEY")

app = Flask(__name__)

BASE_URL = 'https://min-api.cryptocompare.com/data/'


def make_request(endpoint, params):
    try:
        response = requests.get(BASE_URL + endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Request error: {e}")
        return {"error": str(e)}


@app.route("/<cryptocurrency>/latest/<current>", methods=["GET"])
def get_latest_prices(cryptocurrency, current):
    params = {'fsym': cryptocurrency, 'tsyms': current, 'api_key': api_key}
    data = make_request('price', params)
    if "error" in data:
        return jsonify(data), 500
    return jsonify({cryptocurrency: f"{data[current]} {current}"})


@app.route("/<cryptocurrency>/<time>/<current>/<limit>", methods=["GET"])
def get_history_prices(cryptocurrency, time, current, limit):
    if time not in ['hour', 'day']:
        return jsonify({"error": "Invalid time parameter. Use 'hour' or 'day'."}), 400
    
    endpoint = f"v2/histo{time}"
    params = {'fsym': cryptocurrency, 'tsym': current, 'limit': limit, 'api_key': api_key}
    data = make_request(endpoint, params)

    if "error" in data:
        return jsonify(data), 500

    prices = [
        {
            "time": datetime.fromtimestamp(info['time']).strftime('%H:%M' if time == 'hour' else '%Y-%m-%d'),
            "high": info['high'],
            "low": info['low'],
            "close": info['close'],
            "currency": current
        }
        for info in data.get('Data', {}).get('Data', [])
    ]
    return prices


@app.route("/<crypto>/analytics/<currency>/<time>/<limit>", methods=["GET"])
def get_analytics(crypto, time, currency, limit):
    prices = get_history_prices(crypto, time, currency, limit)
    if isinstance(prices, dict) and "error" in prices:
        return jsonify(prices), 500

    df = pd.DataFrame(prices)
    return jsonify({
        "average": df['close'].mean(),
        "median": df['close'].median(),
        "min": df['low'].min(),
        "max": df['high'].max(),
    })


@app.route("/<crypto>/plot/<currency>/<time>/<limit>", methods=["GET"])
def get_plot(crypto, time, currency, limit):
    prices = get_history_prices(crypto, time, currency, limit)
    if isinstance(prices, dict) and "error" in prices:
        return jsonify(prices), 500

    df = pd.DataFrame(prices)

    df['color'] = ['green'] + ['green' if df['close'][i] > df['close'][i - 1] else 'red' for i in range(1, len(df))]
    df['percent_change'] = [0] + [(df['close'][i] - df['close'][i - 1]) / df['close'][i - 1] * 100 for i in range(1, len(df))]

    plt.figure(figsize=(12, 6))

    for i in range(1, len(df)):
        plt.plot(
            [df['time'][i - 1], df['time'][i]],
            [df['close'][i - 1], df['close'][i]],
            color=df['color'][i],
            linewidth=2.5
        )

        plt.text(
            df['time'][i],
            df['close'][i],
            f"{df['percent_change'][i]:+.2f}%",
            color='black',
            ha='center', va='bottom', fontsize=9,
            bbox=dict(facecolor=df['color'][i], alpha=0.3, edgecolor='none', boxstyle='round,pad=0.3')
        )

    plt.xlabel("Time")
    plt.ylabel("Close Price")
    plt.title("Цена крипты")
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)