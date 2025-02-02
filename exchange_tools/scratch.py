import krakenex

def verify_kraken_api(api_key, api_secret):
    # Initialize the Kraken API client
    api = krakenex.API(key=api_key, secret=api_secret)
    
    try:
        # Attempt to retrieve your account balance
        response = api.query_private('Balance')
        
        if response.get('error'):
            print(f"Error: {response['error']}")
            return False
        else:
            print("API key and secret are working correctly.")
            return True
    except Exception as e:
        print(f"An exception occurred: {e}")
        return False

# Replace 'your_api_key' and 'your_api_secret' with your actual Kraken API key and secret
