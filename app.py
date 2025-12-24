
import mysql.connector
from flask import Flask, render_template, request, jsonify, url_for
from flask_cors import CORS
import random

app = Flask(__name__)

# Función de conexión para Railway
def conectar_db():
    """Establece la conexión con la base de datos de Railway"""
    return mysql.connector.connect(
        host='yamabiko.proxy.rlwy.net',
        user='root',
        password='LoMnmisPxQJryOqMgmboWKKPfoZYbrVf',
        database='railway',
        port=11478
    )

# --- RUTAS DE NAVEGACIÓN ---

@app.route('/')
def presentacion(): 
    return render_template('presentacion.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/iniciarSesion')
def iniciarSesion():
    return render_template('iniciarSesion.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/form')
def form():
    return render_template('form.html')

# --- RUTAS DE LA API (Procesamiento de datos) ---

@app.route('/api/registro', methods=['POST'])
def api_registro():
    datos = request.json
    conexion = None
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        id_automatico = random.randint(100, 999999)
        
        # INSERTAR INCLUYENDO EL ID GENERADO
        query = """
            INSERT INTO usuarios (id_usuario, nombre_completo, correo, contrasenia) 
            VALUES (%s, %s, %s, %s)
        """
        valores = (id_automatico, datos['nombre_completo'], datos['correo'], datos['contrasenia'])
        
        cursor.execute(query, valores)
        conexion.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        # Si el ID aleatorio justo existía, intentamos una vez más
        return jsonify({'success': False, 'message': "Error de ID o datos: " + str(e)})
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

# API PARA LOGIN (Sincronizada con Railway)
@app.route('/api/login', methods=['POST'])
def api_login():
    datos = request.json
    conexion = None
    try:
        conexion = conectar_db()
        cursor = conexion.cursor(dictionary=True)
        # Buscamos por correo y contraseña tal cual están en tu tabla
        query = "SELECT * FROM usuarios WHERE correo = %s AND contrasenia = %s"
        cursor.execute(query, (datos['correo'], datos['contrasenia']))
        usuario = cursor.fetchone()
        
        if usuario:
            return jsonify({'success': True, 'user': usuario})
        else:
            return jsonify({'success': False, 'message': 'Correo o contraseña incorrectos'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

# Busca esta línea al final de tu app.py y reemplázala:
# Busca esta línea al final de tu app.py y reemplázala:
if __name__ == '__main__':
    # Usamos os.environ para que Render decida el puerto
    import os
    port = int(os.environ.get('PORT', 8000))
    # host='0.0.0.0' permite que Render "vea" tu app desde afuera
    app.run(host='0.0.0.0', port=port, debug=False)
