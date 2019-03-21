from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from app import app
import csv

ficherotransacciones = "data/transacciones.dat"
fields = ['fecha', 'hora', 'descripcion', 'monedacomprada', 'cantidadcomprada', 'monedapagada', "cantidadpagada"]

@app.route("/")
def index():
    transacciones =open(ficherotransacciones, "r")
    csvreader = csv.reader(transacciones, delimiter=",", quotechar='"')
    movimientos = []
    if csv.reader != "":
        for campos in csvreader:
            camposdict ={}
            for ix, field in enumerate(fields):
                camposdict[field]=campos[ix]
            movimientos.append(camposdict)
    return render_template("index.html", campos=movimientos)
    
@app.route('/nuevacompra', methods=["GET", "POST"])
def  nuevacompra():
    if request.method == "GET":
        return render_template("nuevacompra.html")
    else:
        transacciones = open(ficherotransacciones, "+a")
        nada = "{},{},'{}',{},{},{},{}\n".format(request.form["fecha"],request.form["hora"],request.form["descripcion"],request.form["monedacomprada"],request.form["cantidadcomprada"],request.form["monedapagada"],request.form["cantidadpagada"])
        transacciones.write(nada)
        transacciones.close()
        return redirect(url_for('index'))