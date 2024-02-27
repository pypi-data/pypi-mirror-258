"""
Binance.US API
https://docs.binance.us/?python#request-for-quote
"""

import hashlib
import hmac
import urllib.parse

import requests

api_url = "https://api.binance.us"
account_path = "/api/v3/account"
price_path='/api/v3/ticker/price'
quote_path = "/sapi/v1/otc/quotes"
place_order_path = "/sapi/v1/otc/orders"
order_path = "/sapi/v1/otc/orders"


# get binanceus signature
def get_binanceus_signature(data, secret):
    postdata = urllib.parse.urlencode(data)
    message = postdata.encode()
    byte_key = bytes(secret, 'UTF-8')
    mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return mac


def binanceus_get(uri_path, data, api_key, api_sec):
    headers = {}
    headers['X-MBX-APIKEY'] = api_key
    signature = get_binanceus_signature(data, api_sec)
    params={
        **data,
        "signature": signature,
    }
    resp = requests.get((api_url + uri_path), params=params, headers=headers)
    return resp.json()


# Attaches auth headers and returns results of a POST request
def binanceus_post(uri_path, data, api_key, api_sec):
    headers = {}
    headers['X-MBX-APIKEY'] = api_key
    signature = get_binanceus_signature(data, api_sec)
    payload = {
        **data,
        "signature": signature,
    }
    resp = requests.post((api_url + uri_path), headers=headers, data=payload)
    return resp.json()
