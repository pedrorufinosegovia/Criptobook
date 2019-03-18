from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hola, Mundo"

@app.route('/registro')
def comenzamos():
    return "Ahora ya exsisto"
