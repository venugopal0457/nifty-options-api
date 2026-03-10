from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/nifty")

def nifty():

    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    records = data["records"]["data"]

    max_call = 0
    max_put = 0
    call_strike = 0
    put_strike = 0

    for r in records:

        if "CE" in r and r["CE"]["openInterest"] > max_call:
            max_call = r["CE"]["openInterest"]
            call_strike = r["strikePrice"]

        if "PE" in r and r["PE"]["openInterest"] > max_put:
            max_put = r["PE"]["openInterest"]
            put_strike = r["strikePrice"]

    bias = "BULLISH" if put_strike > call_strike else "BEARISH"

    trade = f"BUY {put_strike} PE" if bias=="BEARISH" else f"BUY {call_strike} CE"

    return jsonify({
        "support": put_strike,
        "resistance": call_strike,
        "bias": bias,
        "trade": trade
    })

app.run(host="0.0.0.0", port=10000)
