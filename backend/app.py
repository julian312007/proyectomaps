import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path
from services.math_service import clasificar_nivel, resolver_pvi_ruta
from services.risk_service import cargar_riesgos
from services.route_service import obtener_ruta
from services.zone_service import obtener_comunas


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / 'frontend'

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path=''
)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'Backend funcionando correctamente'
    })

@app.route('/api/riesgos', methods=['GET'])
def obtener_riesgos():
    try:
        riesgos = cargar_riesgos()
        return jsonify(riesgos)
    except FileNotFoundError as error:
        return jsonify({'error': str(error)}), 500
    except json.JSONDecodeError:
        return jsonify({'error': 'Error al leer datos de riesgos'}), 500

@app.route('/api/ruta-demo', methods=['GET'])
def obtener_ruta_demo():
    try:
        ruta = cargar_ruta_demo()
        return jsonify(ruta)
    except FileNotFoundError as error:
        return jsonify({'error': str(error)}), 500
    except json.JSONDecodeError:
        return jsonify({'error': 'Error al leer datos de ruta demo'}), 500

@app.route('/api/calcular-riesgo-ruta', methods=['POST'])
def calcular_riesgo_ruta():
    request_data = request.get_json(silent=True)
    if not request_data:
        return jsonify({'error': 'Petición inválida: se requiere JSON'}), 400

    riesgo_inicial = request_data.get('riesgo_inicial', 1)
    tramos = request_data.get('tramos', [])
    modelo = request_data.get('modelo', 'no_lineal')

    if not isinstance(tramos, list):
        return jsonify({'error': 'tramos debe ser una lista'}), 400

    try:
        resultado = resolver_pvi_ruta(riesgo_inicial, tramos, modelo)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comunas', methods=['GET'])
def obtener_comunas_endpoint():
    try:
        comunas = obtener_comunas()
        return jsonify(comunas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/ruta", methods=["GET"])
def ruta():
    origen = request.args.get("origen", "").strip()
    destino = request.args.get("destino", "").strip()

    if not origen or not destino:
        return jsonify({
            "error": "Debes ingresar origen y destino"
        }), 400

    try:
        comunas = obtener_comunas()
        ruta_calculada = obtener_ruta(origen, destino, comunas)
        return jsonify(ruta_calculada)

    except Exception as error:
        print(f"Error en /api/ruta: {error}")
        return jsonify({
            "error": "No se pudo obtener la ruta",
            "detalle": str(error)
        }), 500

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
