from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from app import app
import csv
import os

ficherotransacciones = "data/transacciones.dat"
nuevoficherotransacciones = "data/newtransacciones.dat"
fields = ['fecha', 'hora', 'descripcion', 'monedacomprada', 'cantidadcomprada', 'monedapagada', "cantidadpagada"]

def Makedict(lista):
    camposdict = {}
    for ix, field in enumerate(fields):
        camposdict[field] = lista[ix]
    return camposdict

@app.route("/")
def index():
    transacciones =open(ficherotransacciones, "r")
    csvreader = csv.reader(transacciones, delimiter=",", quotechar='"')
    movimientos = []
    if csv.reader != "":
        for campos in csvreader:
            camposdict = Makedict(campos)
            movimientos.append(camposdict)
    return render_template("index.html", campos=movimientos)

@app.route('/modificacompra', methods=["POST"])
def  modificacompra():
    datos = request.form
    transacciones =open(ficherotransacciones, "r")
    newtransacciones = open(nuevoficherotransacciones, "w+")
    registrosleccionado = int(datos['registroseleccionado'])
    linea = transacciones.readline()
    numreg = 0
    while linea != "":  
        if numreg == registrosleccionado:
             linea = "{},{},'{}',{},{},{},{}\n".format(request.form["fecha"],request.form["hora"],request.form["descripcion"],request.form["monedacomprada"],request.form["cantidadcomprada"],request.form["monedapagada"],request.form["cantidadpagada"])   
        
        newtransacciones.write(linea)
        linea = transacciones.readline()
        numreg += 1
    
    transacciones.close()
    newtransacciones.close()
    os.remove(ficherotransacciones)
    os.rename(nuevoficherotransacciones, ficherotransacciones)
        
    return redirect(url_for('index'))

@app.route('/nuevacompra', methods=["GET", "POST"])
def nuevacompra():
    if request.method == "GET":
        if len(request.values) == 0 or request.values['btnselected'] == 'Nueva':
            return render_template("nuevacompra.html")
        else:
            if request.values.get('ix') == None:
                return redirect(url_for('index'))
            ix = int(request.values['ix'])
            transacciones = open(ficherotransacciones, "r")
            csvreader = csv.reader(transacciones, delimiter=",", quotechar='"')
            for numreg, registro in enumerate(csvreader):
                if numreg == ix:
                    camposdict = Makedict(registro)
                    camposdict["registroseleccionado"] = ix
                    return render_template("modicacompra.html", registro = camposdict)
            return "movimiento no encontrado"
    else:
        transacciones = open(ficherotransacciones, "+a")
        nada = "{},{},'{}',{},{},{},{}\n".format(request.form["fecha"],request.form["hora"],request.form["descripcion"],request.form["monedacomprada"],request.form["cantidadcomprada"],request.form["monedapagada"],request.form["cantidadpagada"])
        transacciones.write(nada)
        transacciones.close()
        return redirect(url_for('index'))