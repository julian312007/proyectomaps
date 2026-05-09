import json
from pathlib import Path
from .math_service import calcular_riesgo, clasificar_nivel

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data' / 'riesgos.json'


def cargar_riesgos():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f'Archivo de datos no encontrado: {DATA_PATH}')

    with DATA_PATH.open('r', encoding='utf-8') as archivo:
        zonas = json.load(archivo)

    resultado = []
    for zona in zonas:
        riesgo = calcular_riesgo(zona['criminalidad'], zona['seguridad'])
        nivel = clasificar_nivel(riesgo)
        resultado.append({
            'id': zona['id'],
            'nombre': zona['nombre'],
            'lat': zona['lat'],
            'lng': zona['lng'],
            'criminalidad': zona['criminalidad'],
            'seguridad': zona['seguridad'],
            'riesgo': riesgo,
            'nivel': nivel,
            'descripcion': zona.get('descripcion', ''),
        })

    return resultado
