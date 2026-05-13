import json
from pathlib import Path
from .math_service import modelo_lineal, modelo_no_lineal, clasificar_nivel

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'

def cargar_comunas():
    with open(DATA_DIR / 'comunas_cali.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def calcular_riesgo_comunas(comunas):
    for comuna in comunas:
        derivada_lineal = modelo_lineal(comuna['criminalidad'], comuna['seguridad'])
        derivada_no_lineal = modelo_no_lineal(
            comuna['criminalidad'], comuna['seguridad'], comuna['vigilancia'],
            comuna['iluminacion'], comuna['flujo_personas']
        )
        # Riesgo final aproximado (usando derivada * distancia, pero distancia no definida, usar 1 km)
        riesgo_final = derivada_no_lineal * 1
        nivel = clasificar_nivel(riesgo_final)
        comuna.update({
            'derivada_lineal': round(derivada_lineal, 2),
            'derivada_no_lineal': round(derivada_no_lineal, 2),
            'riesgo_final': round(riesgo_final, 2),
            'nivel': nivel
        })
    return comunas

def obtener_comunas():
    comunas = cargar_comunas()
    return calcular_riesgo_comunas(comunas)