from flask import Flask, request, render_template
from google.cloud import language_v1

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        sentiment = analyze_sentiment(text)
        return render_template('index.html', text=text, sentiment=sentiment)
    return render_template('index.html')

def analyze_sentiment(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.types.Document(content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    return sentiment.score

if __name__ == '__main__':
    app.run(debug=True)  # DON'T use debug=True in production on App Engine
