from flask import Flask
import requests
import os
from gcp_tools.gcp_utils import get_secret
from exchange_tools.exchange_tool import KrakenAPIClient
from exchange_tools.kraken_tools import get_kraken_api


app = Flask(__name__)

@app.route('/')
def hello():
    return """
    <html>
        <head>
            <title>To my Wing Man</title>
        </head>
        <body>
            <h1>Hello Mr. Peters. </h1>
        </body>
    </html>
    """

# @app.route('/test_kraken_access')
def test_connection():
    kraken_api = get_kraken_api()
    client = KrakenAPIClient(kraken_api)
    return client.fetch_assets()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))