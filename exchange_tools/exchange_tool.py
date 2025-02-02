import krakenex

class KrakenAPIClient:
    def __init__(self, api: krakenex.API):
        self.api = api
    def get_balance(self):
        '''fetch balance from Kraken'''
        response = self.api.query_private('Balance')
        if response.get('error'):
            raise Exception(f"Error fetching balance: {response['error']}")
        return response['result']

    def fetch_assets(self):
        '''fetch all assets from Kraken'''
        response = self.api.query_public('Assets')
        if response.get('error'):
            raise Exception(f"Error fetching assets: {response['error']}")
        return response['result']

    def fetch_ticker(self, pair: str):
        """
        Fetch the ticker information for a given currency pair from Kraken.

        Args:
            pair (str): The currency pair to fetch the ticker for (e.g., 'XXBTZUSD').

        Returns:
            dict: The ticker information for the given currency pair.

        Raises:
            Exception: If there is an error fetching the ticker from Kraken.
        """
        '''fetch ticker for a given pair from Kraken'''
        response = self.api.query_public('Ticker', {'pair': pair})
        if response.get('error'):
            raise Exception(f"Error fetching ticker: {response['error']}")
        return response['result'][pair]

    def place_order(self, pair: str, order_type: str, volume: float):
        '''place an order on Kraken with params
        pair: trading pair (e.g., 'XXBTZUSD')
        order_type: 'buy' or 'sell'
        volume: amount to buy/sell
        '''
        response = self.api.query_private('AddOrder', {
            'pair': pair,
            'type': order_type,
            'ordertype': 'market',
            'volume': volume
        })
        if response.get('error'):
            raise Exception(f"Error placing order: {response['error']}")
        return response['result']

class AssetPair:
    def __init__(self, crypto_a: str, crypto_b: str, assets: dict):
        """
        Initializes the ExchangeTool with the given cryptocurrencies and assets.

        Args:
            crypto_a (str): The symbol of the first cryptocurrency.
            crypto_b (str): The symbol of the second cryptocurrency.
            assets (dict): A dictionary containing asset information.

        Attributes:
            crypto_a (str): The symbol of the first cryptocurrency in uppercase.
            crypto_b (str): The symbol of the second cryptocurrency in uppercase.
            assets (dict): A dictionary containing asset information.
        """
        self.crypto_a = crypto_a.upper()
        self.crypto_b = crypto_b.upper()
        self.assets = assets

    def get_pair_symbol(self):
        """
        Generates a trading pair symbol by concatenating the asset IDs of two cryptocurrencies.

        This method retrieves the asset IDs for the cryptocurrencies specified by `crypto_a` and `crypto_b`.
        If either asset ID cannot be found, a ValueError is raised.

        Returns:
            str: The concatenated trading pair symbol of the two cryptocurrencies.

        Raises:
            ValueError: If either `crypto_a` or `crypto_b` is unknown.
        """
        asset_a = self._get_asset_id(self.crypto_a)
        asset_b = self._get_asset_id(self.crypto_b)
        if not asset_a or not asset_b:
            raise ValueError(f"Unknown assets: {self.crypto_a} or {self.crypto_b}")
        return f'{asset_a}{asset_b}'

    def _get_asset_id(self, altname: str):
        """
        Retrieve the asset ID for a given asset alternative name.

        Args:
            altname (str): The alternative name of the asset.

        Returns:
            str or None: The asset ID if found, otherwise None.
        """
        for asset_id, info in self.assets.items():
            if info['altname'] == altname:
                return asset_id
        return None

class TradeExecutor:
    def __init__(self, api_client: KrakenAPIClient):
        """
        Initializes the ExchangeTool with a KrakenAPIClient instance.

        Args:
            api_client (KrakenAPIClient): An instance of KrakenAPIClient to interact with the Kraken API.
        """
        self.api_client = api_client

    def execute_trade(self, crypto_a: str, crypto_b: str, dollar_amount: float):
        """
        Executes a trade between two cryptocurrencies using a specified dollar amount.
        Args:
            crypto_a (str): The symbol of the cryptocurrency to trade from.
            crypto_b (str): The symbol of the cryptocurrency to trade to.
            dollar_amount (float): The amount in dollars to use for the trade.
        Returns:
            dict: The result of the order placed, as returned by the API client.
        """
        assets = self.api_client.fetch_assets()
        asset_pair = AssetPair(crypto_a, crypto_b, assets)
        pair_symbol = asset_pair.get_pair_symbol()

        ticker = self.api_client.fetch_ticker(pair_symbol)
        ask_price = float(ticker['a'][0])

        volume = dollar_amount / ask_price

        order_result = self.api_client.place_order(pair_symbol, 'buy', volume)
        return order_result
