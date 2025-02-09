from flask import Flask
import requests
import os
app = Flask(__name__)

@app.route('/')
def hello():
    return """
    <html>
        <head>
            <title>Anna Gilbert</title>
        </head>
        <body>
            <h1>To Anna Gilbert, my amazing hokis</h1>
            <p>You are my heart, you are my breath.</p>
            <p>You are the beat beat beneath my chest.</p>
            <p>You are the stars that light my night</p>
            <p>I'll follow you whether wrong or right.</p>
        </body>
    </html>
    """

@app.route('/test_connection')
def test_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)  # Test a known website
        if response.status_code == 200:
            return "Connection successful!"
        else:
            return f"Connection failed: Status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Connection failed: {e}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))