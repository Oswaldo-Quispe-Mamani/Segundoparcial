from flask import Flask, session, render_template, request, redirect, url_for
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'super_secret_key'  

@app.before_request
def init_session():
    if 'productos' not in session:
        session['productos'] = []

@app.route('/')
def index():
    productos = session['productos']
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        id = str(uuid.uuid4())
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']
        
        nuevo_producto = {
            'id': id,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }

        
        productos = session['productos']
        productos.append(nuevo_producto)
        session['productos'] = productos  

        return redirect(url_for('index'))
    
    return render_template('agregar.html')

@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = session['productos']
    producto = next((prod for prod in productos if prod['id'] == id), None)

    if not producto:
        return redirect(url_for('index'))

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']

        session['productos'] = productos
        session.modified = True 
        return redirect(url_for('index'))
    return render_template('editar.html', producto=producto)
    

@app.route('/eliminar/<id>', methods=['POST'])
def eliminar_producto(id):
    productos = session['productos']
    session['productos'] = [prod for prod in productos if prod['id'] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)