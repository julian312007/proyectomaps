import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path
from services.math_service import clasificar_nivel
from services.risk_service import cargar_riesgos
from services.route_service import cargar_ruta_demo

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

    riesgo_inicial = request_data.get('riesgo_inicial')
    tramos = request_data.get('tramos')

    if riesgo_inicial is None or not isinstance(tramos, list):
        return jsonify({'error': 'Petición inválida: falta riesgo_inicial o tramos'}), 400

    try:
        riesgo_actual = float(riesgo_inicial)
    except (TypeError, ValueError):
        return jsonify({'error': 'riesgo_inicial debe ser un número'}), 400

    if riesgo_actual < 0:
        return jsonify({'error': 'riesgo_inicial no puede ser negativo'}), 400

    resultados = []

    for tramo in tramos:
        if not all(key in tramo for key in ('tramo', 'criminalidad', 'seguridad', 'distancia')):
            return jsonify({'error': 'Cada tramo debe contener tramo, criminalidad, seguridad y distancia'}), 400

        try:
            criminalidad = float(tramo['criminalidad'])
            seguridad = float(tramo['seguridad'])
            distancia = float(tramo['distancia'])
        except (TypeError, ValueError):
            return jsonify({'error': 'Los valores de tramo deben ser numéricos'}), 400

        riesgo_tramo = round((0.5 * criminalidad - 0.3 * seguridad) * distancia, 2)
        riesgo_actual = round(riesgo_actual + riesgo_tramo, 2)
        nivel = clasificar_nivel(riesgo_actual)

        resultados.append({
            'tramo': tramo['tramo'],
            'riesgo_tramo': riesgo_tramo,
            'riesgo_acumulado': riesgo_actual,
            'nivel': nivel,
        })

    nivel_final = clasificar_nivel(riesgo_actual)

    return jsonify({
        'riesgo_inicial': float(request_data.get('riesgo_inicial')),
        'riesgo_final': riesgo_actual,
        'nivel_final': nivel_final,
        'tramos': resultados,
    })

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
