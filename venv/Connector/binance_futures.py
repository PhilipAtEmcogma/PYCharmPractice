import logging

import requests
import time
from urllib.parse import urlencode

import hmac
import hashlib

logger = logging.getLogger()

class BinanceFuturesClient:
    #__init__() is a constructor
    def __init__(self, public_key, secret_key, testnet):
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
        else:
            self.base_url = "https://fapi.binance.com"

        self.public_key = public_key
        self.secret_key = secret_key

        self.headers = {'X-MBX-APIKEY': self.public_key}

        self.prices = dict()

        logger.info("Binance Futures Client successfully initialized")

    def generate_signature(self,data):
        #self.secret_key.encode() convert a string to a byte
        # urlencode(data).encode(),  urlencode(data) convert to a query string, then convert string to byte using .encode()
        return hmac.new(self.secret_key.encode(), urlencode(data).encode(), hashlib.sha256).hexdigest()

    def make_request(self, method, endpoint, data):
        if method == "GET":
            response = requests.get(self.base_url + endpoint, params=data, headers=self.headers)
        elif method == "POST":
            response = requests.post(self.base_url + endpoint, params=data, headers=self.headers)
        elif method == "DELETE":
            response = requests.delete(self.base_url + endpoint, params=data, headers=self.headers)
        else:
            raise ValueError

        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Error while making %s request to %s: %s (error code %s)",
                         method, endpoint, response.json(), response.status_code)
            return None

    def get_contracts(self):
        exchange_info = self.make_request("GET", "/fapi/v1/exchangeInfo", None)

        contracts = dict()

        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                contracts[contract_data['pair']] = contract_data

        return contracts

    def get_historical_candles(self, symbol, interval):
        data = dict()
        data['symbol'] = symbol
        data['interval'] = interval
        data['limit'] = 1000

        raw_candles = self.make_request("GET", "/fapi/v1/klines", data)

        candles = []

        if raw_candles is not None:
            for c in raw_candles:
                candles.append([c[0], float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5])])

        return candles

    def get_bid_ask(self, symbol):
        data = dict()
        data['symbol'] = symbol
        ob_data = self.make_request("GET", "/fapi/v1/ticker/bookTicker", data)

        if ob_data is not None:
            if symbol not in self.prices:
                self.prices[symnol] = {'bid':float(ob_data['bidPrice']), 'ask':float(ob_data['askPrice'])}
            else:
                self.prices[symbol]['bid'] = float(ob_data['bidPrice'])
                self.prices[symbol]['ask'] = float(ob_data['askPrice'])


        """
        # the link below, anything after ? is a parameter, it can take more than 1 parameter,
        # simply by putting a &, for example below. getting infor for BTCUSD and ADAUSDT
        "https://testnet.binancefuture.com/fapi/v1/ticker/bookTicker?symbol=BTCUSDT&symbol=ADAUSDT"
        """

        return self.prices[symbol]

    def get_balance(self):
        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)
        balances = dict()

        account_data = self.make_request("GET","/fapi/v2/account",data)

        #if request is successful, loop through the list of assets and finally return the list of assets
        if account_data is not None:
            for a in account_data['assets']:
                balances[a['asset']] = a
        return balances

    def place_order(self, symbol, side, quantity, order_type, price=None, tif=None):
        data = dict()
        data['symbol'] = symbol
        data['side'] = side
        data['quantity'] = quantity
        data['type'] = order_type

        if price is not None:
            data['price'] = price

        # tif = time in force, specifies how long your order will remain open before it is canceled
        if tif is not None:
            data['timeInForce'] = tif

        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)

        order_status = self.make_request("POST", "/fapi/v1/order", data)

        return order_status

    def cancel_order(self,symbol,order_id):
        data = dict()
        data['orderId'] = order_id
        data['symbol'] = symbol

        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)

        order_status = self.make_request("DELETE", "/fapi/v1/order", data)

        return order_status

    def get_order_status(self, symbol, order_id):
        data = dict()
        data['timestamp'] = int(time.time()*1000)
        data['symbol']=symbol
        data['orderId']=order_id
        data['signature'] = self.generate_signature(data)

        order_status = self.make_request("GET","/fapi/v1/order", data)
        return order_status
"""
def get_contracts():
    response_object = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")
    # print(response_object.status_code)
    # pprint.pprint(response_object.json())
    # pprint.pprint(response_object.json()['symbols'])
    contracts = []

    for contract in response_object.json()['symbols']:
        # pprint.pprint(contract)
        # print(contract['pair'])
        contracts.append(contract['pair'])

    return contracts

print(get_contracts())
"""