import pandas as pd
from datetime import datetime as dt, timedelta
from gcp_tools.gcp_utils import get_secret
from exchange_tools.kraken_tools import get_kraken_api, get_trading_pair_symbol
from exchange_tools.exchange_tool import KrakenAPIClient, AssetPair, TradeExecutor
from common.date_utils import *

    

def prepare_time_range_parameters(start_datetime: str, end_datetime: str):
    '''
    start_datetime: yyyy-mm-hh hh:mm:ss
    end_datetime: yyyy-mm-hh hh:mm:ss
    returns start_unix_timestamp, end_unix_timestamp
    '''
    start_unix_timestamp = datetime_str_to_unix(start_datetime)
    end_unix_timestamp = datetime_str_to_unix(end_datetime)
    return start_unix_timestamp, end_unix_timestamp

def main(start_unix_timestamp, end_unix_timestamp):
    kraken_api = KrakenAPIClient(get_kraken_api())
    
    
    assets = kraken_api.fetch_assets()
    asset_pair = AssetPair('XBT', 'USD', assets)
    pair_symbol = asset_pair.get_pair_symbol()
    asset_history = kraken_api.fetch_asset_history(pair_symbol,start_unix_timestamp, end_unix_timestamp )


    asset_history_df = pd.DataFrame(asset_history['XXBTZUSD'], columns=['price', 'volume', 'time', 'buy_sell', 'market_limit', 'misc', 'trade_id'])
    asset_history_df['time'] = pd.to_datetime(asset_history_df['time'], unit='s')
    asset_history_df['price'] = pd.to_numeric(asset_history_df['price'])
    asset_history_df = asset_history_df.sort_values('time')
    return asset_history_df

if __name__ == '__main__':
    to_time = dt.now()
    from_time = to_time - timedelta(minutes=30)
    start_unix_timestamp, end_unix_timestamp = prepare_time_range_parameters(datetime_to_str(from_time), datetime_to_str(to_time))
    main(start_unix_timestamp, end_unix_timestamp)
    
