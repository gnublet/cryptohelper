import urllib
import json, requests, time, hmac
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import hashlib


# functions (cryptocompare)
def get_coins():
    """Gets list of coins supported by cryptocompare api
    
    Args: 
        None
    Returns:
        coins (DataFrame)
    """
    url = "https://min-api.cryptocompare.com/data/all/coinlist"
    r = requests.get(url)
    j = json.loads(r.text)
    df_coins = pd.DataFrame.from_dict(j['Data']).transpose()
    return df_coins
#     return r.text
def get_histohour(fsym = 'BTC', tsym = 'USD', e = 'CCCAGG', limit = 1920, optional_params = {}):
    """Gets hourly pricing info for given exchange
    
    Args:
        Required:
            fsym (str): From symbol
            tsym (str): To symbol
            e (str): Name of exchange
        Optional:
            extraParams (str): Name of app
            sign (bool): if true, server will sign requests
            tryConvention (bool): if false, get values without conversion
            aggregate (int): 
            limit (int): default: 168, max: 2000 (new default: 1920 (80 days))
            toTs (timestamp):
    
        Valid exchanges (e): 
            Cryptsy, BTCChina, Bitstamp, BTER, OKCoin, Coinbase, Poloniex, Cexio, BTCE, BitTrex, Kraken, 
            Bitfinex, Yacuna, LocalBitcoins, Yunbi, itBit, HitBTC, btcXchange, BTC38, Coinfloor, Huobi, 
            CCCAGG, LakeBTC, ANXBTC, Bit2C, Coinsetter, CCEX, Coinse, MonetaGo, Gatecoin, Gemini, CCEDK, 
            Cryptopia, Exmo, Yobit, Korbit, BitBay, BTCMarkets, Coincheck, QuadrigaCX, BitSquare, 
            Vaultoro, MercadoBitcoin, Bitso, Unocoin, BTCXIndia, Paymium, TheRockTrading, bitFlyer, 
            Quoine, Luno, EtherDelta, bitFlyerFX, TuxExchange, CryptoX, Liqui, MtGox, BitMarket, LiveCoin, 
            Coinone, Tidex, Bleutrade, EthexIndia, Bithumb, CHBTC, ViaBTC, Jubi, Zaif, Novaexchange, 
            WavesDEX, Binance, Lykke, Remitano, Coinroom, Abucoins, BXinth, Gateio, HuobiPro, OKEX
    
    Returns:
        history (str) hourly price history from fsym to tsym
    """
    url = "https://min-api.cryptocompare.com/data/histohour"
    params = {'fsym':fsym, 'tsym':tsym, 'e': e, 'limit': limit}
    for k,v in optional_params.items():
        params[k] = v
        
    r = requests.get(url = url, params = params)
    return r.text

def get_top_pairs(fsym='BTC', tsym='USD', limit=5, optional_params = {}):
    """ get the top [limit] pairs (from fsym to tsym)
    Args:
        Requried:
            fsym (str): From symbol 
            tsym (str): To symbol
        Optional:
            limit (int): number of pairs to return: default (5)
            sign (bool): if true, server will sign request
    
    Return:
        top pairs (str): get top pairs by volume for a currency (using aggregate data). 

    """
    url = "https://min-api.cryptocompare.com/data/top/pairs"
    params = {'fsym': fsym, 'tsym': tsym, 'limit': limit}
    for k,v in optional_params.items():
        params[k] = v
        
    r = requests.get(url=url, params=params)
    return r.text

# watched_symbols = []
def create_watched_symbols(symbols=[], all_symbols=[]):
    watched_symbols = []
    for sym in symbols:
        if sym in all_symbols:
            watched_symbols.append(sym)
    return watched_symbols

# download histohour data for watched symbols
def download_data(watched_symbols=[]):
    """download hourly data for the watched symbols to files
    
    Args:
        watched_symbols (list of strs)
    Returns: 
        None (saves files under data folder (TODO: for user)"""

    for sym in watched_symbols:
        # sym = 'BTC'
        time.sleep(10)
        limit = 1920 # 80 days
        histohour = json.loads(get_histohour(fsym = sym, tsym = 'USD', e = 'CCCAGG'))
        histohour_json = json.dumps(histohour['Data'])
        df_histohour = pd.read_json(histohour_json)
        df_histohour.transpose()
        print("writing {}_histohour_{}.csv to file ... ".format(sym, limit))
        df_histohour.to_csv("data/{}_histohour_{}.csv".format(sym, limit), columns = ['close','high','low','open','time','volumefrom','volumeto'])
        print("done")
        # correlations between watched symbols
        
def fill_watched_histohours(watched_symbols=[]):
    import datetime
    dfs_histohour = {} # dict of dataframes
    for sym in watched_symbols:
    #     temp_df = pd.read_csv("data/{}_histohour_1920.csv".format(sym))
        temp_df = pd.read_csv("data/{}_histohour_1920.csv".format(sym), usecols=['close','high','low','open','time','volumefrom','volumeto'])
        temp_df['time'] = temp_df['time'].map(lambda x: datetime.datetime.utcfromtimestamp(x))
        temp_df = temp_df.set_index('time') #set time column as the index
        dfs_histohour[sym] = temp_df
    return dfs_histohour

def get_prices(fsyms = ['BTC', 'LTC', 'ADA', 'XRP'], tsyms = ['USD'], e = 'CCCAGG', optional_params = {}):
    """ get price of symbols (from fsyms to tsyms)
    Args:
        fsyms (list): list of cryptos to convert from
        tsyms (list): list of cryptos to convert to
        e: (str) exchange
        
        Valid exchanges (e): 
                Cryptsy, BTCChina, Bitstamp, BTER, OKCoin, Coinbase, Poloniex, Cexio, BTCE, BitTrex, Kraken, 
                Bitfinex, Yacuna, LocalBitcoins, Yunbi, itBit, HitBTC, btcXchange, BTC38, Coinfloor, Huobi, 
                CCCAGG, LakeBTC, ANXBTC, Bit2C, Coinsetter, CCEX, Coinse, MonetaGo, Gatecoin, Gemini, CCEDK, 
                Cryptopia, Exmo, Yobit, Korbit, BitBay, BTCMarkets, Coincheck, QuadrigaCX, BitSquare, 
                Vaultoro, MercadoBitcoin, Bitso, Unocoin, BTCXIndia, Paymium, TheRockTrading, bitFlyer, 
                Quoine, Luno, EtherDelta, bitFlyerFX, TuxExchange, CryptoX, Liqui, MtGox, BitMarket, LiveCoin, 
                Coinone, Tidex, Bleutrade, EthexIndia, Bithumb, CHBTC, ViaBTC, Jubi, Zaif, Novaexchange, 
                WavesDEX, Binance, Lykke, Remitano, Coinroom, Abucoins, BXinth, Gateio, HuobiPro, OKEX
    Return:
        current prices (DataFrame)
    """
    url = "https://min-api.cryptocompare.com/data/pricemulti"
    tsym_string = ','.join(tsyms)
    fsym_string = ','.join(fsyms)
    params = {'fsyms': fsym_string, 'tsyms': tsym_string, 'e': e}
    for k,v in optional_params.items():
        params[k] = v
        
    r = requests.get(url=url, params=params)
    j = json.loads(r.text)
    df = pd.DataFrame.from_dict(j).transpose()
    return df

def get_prices_full(fsyms = ['BTC', 'LTC', 'ADA', 'XRP'], tsyms = ['USD'], e = 'CCCAGG', optional_params = {}):
    """ get price of symbols (from fsyms to tsyms)
    Args:
        fsyms (list): list of cryptos to convert from
        tsyms (list): list of cryptos to convert to
        e: (str) exchange
        
        Valid exchanges (e): 
                Cryptsy, BTCChina, Bitstamp, BTER, OKCoin, Coinbase, Poloniex, Cexio, BTCE, BitTrex, Kraken, 
                Bitfinex, Yacuna, LocalBitcoins, Yunbi, itBit, HitBTC, btcXchange, BTC38, Coinfloor, Huobi, 
                CCCAGG, LakeBTC, ANXBTC, Bit2C, Coinsetter, CCEX, Coinse, MonetaGo, Gatecoin, Gemini, CCEDK, 
                Cryptopia, Exmo, Yobit, Korbit, BitBay, BTCMarkets, Coincheck, QuadrigaCX, BitSquare, 
                Vaultoro, MercadoBitcoin, Bitso, Unocoin, BTCXIndia, Paymium, TheRockTrading, bitFlyer, 
                Quoine, Luno, EtherDelta, bitFlyerFX, TuxExchange, CryptoX, Liqui, MtGox, BitMarket, LiveCoin, 
                Coinone, Tidex, Bleutrade, EthexIndia, Bithumb, CHBTC, ViaBTC, Jubi, Zaif, Novaexchange, 
                WavesDEX, Binance, Lykke, Remitano, Coinroom, Abucoins, BXinth, Gateio, HuobiPro, OKEX
    Return:
        current prices (DataFrame)
    """
    url = "https://min-api.cryptocompare.com/data/pricemultifull"
    tsym_string = ','.join(tsyms)
    fsym_string = ','.join(fsyms)
    params = {'fsyms': fsym_string, 'tsyms': tsym_string, 'e': e}
    for k,v in optional_params.items():
        params[k] = v
        
    r = requests.get(url=url, params=params)
    j = json.loads(r.text)
    j = j['DISPLAY']
    j_normalized = pd.io.json.json_normalize(j, record_path = 'USD')
    df = pd.DataFrame.from_dict(j_normalized).transpose()
    return df

def bittrex_get_balance(api_key, api_secret):
    """Get your total balances for your bittrex account
    
    args:
        required:
            api_key (str)
            api_secret (str)
    return:
        results (DataFrame) of balance information for each crypto
    """
    nonce = int(time.time()*1000)
    url = "https://bittrex.com/api/v1.1/account/getbalances?apikey={}&nonce={}".format(api_key, nonce)
    # url = 'https://bittrex.com/api/v1.1/account/getbalances'
    sign = hmac.new(api_secret.encode('utf-8'), url.encode('utf-8'), hashlib.sha512).hexdigest()
    headers = {'apisign': sign}
    r = requests.get(url, headers=headers)
    j = json.loads(r.text)
    results = j['result']
    df = pd.DataFrame.from_dict(results)
    return df

def binance_get_balance(api_key, api_secret):
    url = 'https://api.binance.com/api/v3/account'

    headers = {'X-MBX-APIKEY' : api_key}
    timestamp = int(time.time()*1000)
    payload = {'timestamp':timestamp}
    querystring = urllib.parse.urlencode(payload)
    # print(urllib.parse.urlencode(payload))
    signature = hmac.new(api_secret.encode('utf-8'), querystring.encode('utf-8'), hashlib.sha256).hexdigest()

    payload['signature'] = signature
    r = requests.get(url, headers=headers, params=payload)
    j = json.loads(r.text)
    if 'balances' in j:
        return j['balances']
    else:
        return j