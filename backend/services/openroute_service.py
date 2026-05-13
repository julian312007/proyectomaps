import requests
import os
import polyline
from dotenv import load_dotenv

load_dotenv()
ORS_API_KEY = os.getenv('ORS_API_KEY')

def geocodificar_lugar(texto):
    url = f"https://api.openrouteservice.org/geocode/search"
    params = {
        'api_key': ORS_API_KEY,
        'text': texto,
        'size': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            coords = data['features'][0]['geometry']['coordinates']
            return [coords[1], coords[0]]  # [lat, lng]
    return None

def obtener_ruta_ors(origen, destino):
    origen_coords = geocodificar_lugar(f"{origen}, Cali, Colombia")
    destino_coords = geocodificar_lugar(f"{destino}, Cali, Colombia")

    if not origen_coords or not destino_coords:
        return None

    url = f"https://api.openrouteservice.org/v2/directions/driving-car"
    body = {
        "coordinates": [
            [origen_coords[1], origen_coords[0]],  # [lng, lat]
            [destino_coords[1], destino_coords[0]]
        ]
    }
    headers = {
        'Authorization': ORS_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'routes' in data and data['routes']:
            route = data['routes'][0]
            geometry_encoded = route['geometry']
            puntos = polyline.decode(geometry_encoded)  # Decodifica a [lat, lng]
            distancia = route['summary']['distance'] / 1000  # km
            duracion = route['summary']['duration'] / 60  # minutes
            return {
                'puntos': puntos,
                'distancia_total': distancia,
                'duracion_estimada': duracion
            }
    return None

def dividir_ruta_en_tramos(puntos, comunas):
    tramos = []
    for i in range(len(puntos) - 1):
        inicio = puntos[i]
        fin = puntos[i + 1]
        # Calcular distancia aproximada (simple)
        distancia = ((fin[0] - inicio[0])**2 + (fin[1] - inicio[1])**2)**0.5 * 111  # km approx
        # Encontrar comuna más cercana
        comuna = encontrar_comuna_por_punto((inicio[0] + fin[0])/2, (inicio[1] + fin[1])/2, comunas)
        tramos.append({
            'tramo': i + 1,
            'inicio': inicio,
            'fin': fin,
            'distancia': distancia,
            'comuna': comuna['nombre'] if comuna else 'Desconocida',
            'criminalidad': comuna['criminalidad'] if comuna else 5,
            'seguridad': comuna['seguridad'] if comuna else 5,
            'vigilancia': comuna['vigilancia'] if comuna else 5,
            'iluminacion': comuna['iluminacion'] if comuna else 5,
            'flujo_personas': comuna['flujo_personas'] if comuna else 5
        })
    return tramos

def encontrar_comuna_por_punto(lat, lng, comunas):
    min_dist = float('inf')
    closest = None
    for comuna in comunas:
        # Centroide aproximado
        coords = comuna['coordenadas']
        center_lat = sum(c[0] for c in coords) / len(coords)
        center_lng = sum(c[1] for c in coords) / len(coords)
        dist = ((lat - center_lat)**2 + (lng - center_lng)**2)**0.5
        if dist < min_dist:
            min_dist = dist
            closest = comuna
    return closest