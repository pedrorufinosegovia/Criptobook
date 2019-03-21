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
        if request.values['btnselected'] == 'Nueva':
            return render_template("nuevacompra.html")
        else:
            ix = request.values['ix']
            ix = float(ix)
            transacciones = open(ficherotransacciones, "r")
            csvreader = csv.reader(transacciones, delimiter=",", quotechar='"')
            for numreg, registro in enumerate(csvreader):
                if numreg == ix:
                    camposdict ={}
                    for ix, field in enumerate(fields):
                        camposdict[field] = registro[ix]
                    return render_template("modicacompra.html", registro = camposdict)
            return "movimiento no encontrado"
    else:
        transacciones = open(ficherotransacciones, "+a")
        nada = "{},{},'{}',{},{},{},{}\n".format(request.form["fecha"],request.form["hora"],request.form["descripcion"],request.form["monedacomprada"],request.form["cantidadcomprada"],request.form["monedapagada"],request.form["cantidadpagada"])
        transacciones.write(nada)
        transacciones.close()
        return redirect(url_for('index'))