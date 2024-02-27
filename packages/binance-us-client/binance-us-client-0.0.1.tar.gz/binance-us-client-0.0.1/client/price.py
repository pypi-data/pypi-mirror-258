from decimal import Decimal

import requests

from base_api import api_url, price_path


def get_symbol_price(symbol: str) -> Decimal:
    resp = requests.get(f'{api_url}{price_path}?symbol={symbol}')
    return Decimal(resp.json()['price'])


def get_coin_price(coin: str) -> Decimal:
    """
    USDT USD 价格为 1
    :param coin:
    :return:
    """
    if coin == 'USDT' or coin == 'USD':
        return Decimal(1)
    return get_symbol_price(f'{coin}USDT')


def batch_get_symbol_price(symbols: list[str]) -> dict:
    """
    :param symbols: symbol list
    :return: symbol -> price dict
    """
    return dict(zip(symbols, [get_symbol_price(symbol) for symbol in symbols]))


def batch_get_coin_price(coins: list[str]) -> dict:
    """
    :param coins: coin list
    :return: coin -> pice dict
    """
    return dict(zip(coins, [get_coin_price(coin) for coin in coins]))


if __name__ == '__main__':
    print(get_symbol_price('BTCUSDT'))
    print(get_coin_price('BTC'))
    print(batch_get_symbol_price(['BTCUSDT', 'ETHUSDT']))
    print(batch_get_coin_price(['BTC', 'ETH']))
