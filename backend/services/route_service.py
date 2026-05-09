import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data' / 'ruta_demo.json'


def cargar_ruta_demo():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f'Archivo de datos no encontrado: {DATA_PATH}')

    with DATA_PATH.open('r', encoding='utf-8') as archivo:
        ruta = json.load(archivo)

    puntos = ruta.get('puntos', [])
    distancia_total = sum(punto.get('distancia', 0) for punto in puntos)

    return {
        'puntos': puntos,
        'distancia_total': round(distancia_total, 2),
    }
