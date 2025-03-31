from flask import Flask, render_template, url_for
from googletrans import Translator
import requests 
import logging


logging.basicConfig(filename='/tmp/app.log', level=logging.INFO)



translator = Translator()

data = None
def getData(topic):
    url = "https://openlibrary.org/search.json"

    params = {"q": f"subject:{topic}", "limit":15}

    respuesta = requests.get(url, params=params)
    print("Data Recevied")
    data = []

    if respuesta.status_code == 200:
        respuesta = respuesta.json()
        n = 0
        for value in respuesta['docs']:
            data.append({'title': translator.translate(value['title'], src="auto", dest='es').text, 'author_name': value['author_name'][0], 'cover_i': value['cover_i']}) 
            n+=1
        return data
    else: 
        return None


app = Flask(__name__)

@app.route('/')
def root():
    global data
    if not data:
        data = getData('fiction')

    return render_template("index.html", books=data)


@app.route('/test')
def test():
    data = getData('fiction')
    return data

app.run(port=8888, debug=True, host="0.0.0.0")
