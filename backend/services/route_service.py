import json
import math
import os
import unicodedata
from pathlib import Path

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
COMUNAS_PATH = DATA_DIR / "comunas_cali.json"

load_dotenv(BASE_DIR / ".env")

ORS_API_KEY = os.getenv("ORS_API_KEY")

CALI_BOUNDS = {
    "min_lon": -76.65,
    "min_lat": 3.30,
    "max_lon": -76.40,
    "max_lat": 3.55,
}


LUGARES_CALI = {
    # Lugares generales
    "cali": "Cali, Valle del Cauca, Colombia",
    "centro": "Plaza de Cayzedo, Cali, Colombia",
    "plaza de cayzedo": "Plaza de Cayzedo, Cali, Colombia",
    "san nicolas": "Barrio San Nicolas, Cali, Colombia",
    "la ermita": "Iglesia La Ermita, Cali, Colombia",
    "boulevard": "Bulevar del Rio, Cali, Colombia",
    "bulevar del rio": "Bulevar del Rio, Cali, Colombia",

    # Transporte
    "terminal": "Terminal de Transportes de Cali, Cali, Colombia",
    "terminal de transportes": "Terminal de Transportes de Cali, Cali, Colombia",
    "estacion universidades": "Estacion MIO Universidades, Cali, Colombia",
    "estacion san bosco": "Estacion MIO San Bosco, Cali, Colombia",
    "estacion santa librada": "Estacion MIO Santa Librada, Cali, Colombia",

    # Universidades
    "univalle": "Universidad del Valle sede Melendez, Cali, Colombia",
    "universidad del valle": "Universidad del Valle sede Melendez, Cali, Colombia",
    "univalle melendez": "Universidad del Valle sede Melendez, Cali, Colombia",
    "icesi": "Universidad Icesi, Cali, Colombia",
    "javeriana": "Pontificia Universidad Javeriana Cali, Cali, Colombia",
    "autonoma": "Universidad Autonoma de Occidente, Cali, Colombia",
    "universidad autonoma": "Universidad Autonoma de Occidente, Cali, Colombia",
    "usc": "Universidad Santiago de Cali, Cali, Colombia",
    "santiago de cali": "Universidad Santiago de Cali, Cali, Colombia",

    # Centros comerciales
    "chipichape": "Centro Comercial Chipichape, Cali, Colombia",
    "unicentro": "Centro Comercial Unicentro Cali, Cali, Colombia",
    "jardin plaza": "Centro Comercial Jardin Plaza, Cali, Colombia",
    "jardín plaza": "Centro Comercial Jardin Plaza, Cali, Colombia",
    "palmetto": "Centro Comercial Palmetto Plaza, Cali, Colombia",
    "cosmocentro": "Centro Comercial Cosmocentro, Cali, Colombia",
    "rio cauca": "Centro Comercial Rio Cauca, Cali, Colombia",
    "la estacion": "Centro Comercial La Estacion, Cali, Colombia",
    "la estación": "Centro Comercial La Estacion, Cali, Colombia",

    # Oeste / ladera
    "san antonio": "Barrio San Antonio, Cali, Colombia",
    "el penon": "Barrio El Peñon, Cali, Colombia",
    "el peñon": "Barrio El Peñon, Cali, Colombia",
    "granada": "Barrio Granada, Cali, Colombia",
    "juanambu": "Barrio Juanambu, Cali, Colombia",
    "juanambú": "Barrio Juanambu, Cali, Colombia",
    "centenario": "Barrio Centenario, Cali, Colombia",
    "santa teresita": "Barrio Santa Teresita, Cali, Colombia",
    "arboledas": "Barrio Arboledas, Cali, Colombia",
    "normandia": "Barrio Normandia, Cali, Colombia",
    "normandía": "Barrio Normandia, Cali, Colombia",
    "terron colorado": "Barrio Terron Colorado, Cali, Colombia",
    "terrón colorado": "Barrio Terron Colorado, Cali, Colombia",
    "vista hermosa": "Barrio Vista Hermosa, Cali, Colombia",
    "siloe": "Barrio Siloe, Cali, Colombia",
    "siloé": "Barrio Siloe, Cali, Colombia",
    "belen": "Barrio Belen, Cali, Colombia",
    "belén": "Barrio Belen, Cali, Colombia",
    "brisas de mayo": "Barrio Brisas de Mayo, Cali, Colombia",

    # Norte
    "la flora": "Barrio La Flora, Cali, Colombia",
    "la campina": "Barrio La Campiña, Cali, Colombia",
    "la campiña": "Barrio La Campiña, Cali, Colombia",
    "prados del norte": "Barrio Prados del Norte, Cali, Colombia",
    "versalles": "Barrio Versalles, Cali, Colombia",
    "san vicente": "Barrio San Vicente, Cali, Colombia",
    "santa monica": "Barrio Santa Monica, Cali, Colombia",
    "santa mónica": "Barrio Santa Monica, Cali, Colombia",
    "el bosque": "Barrio El Bosque, Cali, Colombia",
    "menga": "Barrio Menga, Cali, Colombia",
    "floralia": "Barrio Floralia, Cali, Colombia",
    "petecuy": "Barrio Petecuy, Cali, Colombia",
    "chiminangos": "Barrio Chiminangos, Cali, Colombia",
    "los guaduales": "Barrio Los Guaduales, Cali, Colombia",
    "salomia": "Barrio Salomia, Cali, Colombia",
    "salomía": "Barrio Salomia, Cali, Colombia",

    # Centro ampliado
    "san cayetano": "Barrio San Cayetano, Cali, Colombia",
    "san bosco": "Barrio San Bosco, Cali, Colombia",
    "santa rosa": "Barrio Santa Rosa, Cali, Colombia",
    "libertadores": "Barrio Libertadores, Cali, Colombia",
    "miraflores": "Barrio Miraflores, Cali, Colombia",
    "tequendama": "Barrio Tequendama, Cali, Colombia",
    "eucaristico": "Barrio Eucaristico, Cali, Colombia",
    "eucarístico": "Barrio Eucaristico, Cali, Colombia",
    "olimpico": "Barrio Olimpico, Cali, Colombia",
    "olímpico": "Barrio Olimpico, Cali, Colombia",
    "colseguros": "Barrio Colseguros, Cali, Colombia",
    "departamental": "Barrio Departamental, Cali, Colombia",

    # Oriente / Aguablanca
    "aguablanca": "Distrito de Aguablanca, Cali, Colombia",
    "distrito de aguablanca": "Distrito de Aguablanca, Cali, Colombia",
    "marroquin": "Barrio Marroquin, Cali, Colombia",
    "marroquín": "Barrio Marroquin, Cali, Colombia",
    "el poblado": "Barrio El Poblado, Cali, Colombia",
    "el poblado i": "Barrio El Poblado I, Cali, Colombia",
    "el poblado ii": "Barrio El Poblado II, Cali, Colombia",
    "los comuneros": "Barrio Los Comuneros, Cali, Colombia",
    "el vergel": "Barrio El Vergel, Cali, Colombia",
    "el diamante": "Barrio El Diamante, Cali, Colombia",
    "el retiro": "Barrio El Retiro, Cali, Colombia",
    "antonio narino": "Barrio Antonio Nariño, Cali, Colombia",
    "antonio nariño": "Barrio Antonio Nariño, Cali, Colombia",
    "mojica": "Barrio Mojica, Cali, Colombia",
    "manuela beltran": "Barrio Manuela Beltran, Cali, Colombia",
    "manuela beltrán": "Barrio Manuela Beltran, Cali, Colombia",
    "desepaz": "Barrio Desepaz, Cali, Colombia",
    "potrero grande": "Barrio Potrero Grande, Cali, Colombia",
    "valle grande": "Barrio Valle Grande, Cali, Colombia",
    "calipso": "Barrio Calipso, Cali, Colombia",
    "el vallado": "Barrio El Vallado, Cali, Colombia",
    "ciudad cordoba": "Barrio Ciudad Cordoba, Cali, Colombia",
    "ciudad córdoba": "Barrio Ciudad Cordoba, Cali, Colombia",
    "ciudad 2000": "Barrio Ciudad 2000, Cali, Colombia",

    # Nororiente
    "las ceibas": "Barrio Las Ceibas, Cali, Colombia",
    "la base": "Barrio La Base, Cali, Colombia",
    "el troncal": "Barrio El Troncal, Cali, Colombia",
    "santa monica popular": "Barrio Santa Monica Popular, Cali, Colombia",
    "santa mónica popular": "Barrio Santa Monica Popular, Cali, Colombia",
    "la independencia": "Barrio La Independencia, Cali, Colombia",
    "el rodeo": "Barrio El Rodeo, Cali, Colombia",
    "la floresta": "Barrio La Floresta, Cali, Colombia",
    "atanasio girardot": "Barrio Atanasio Girardot, Cali, Colombia",
    "chapinero": "Barrio Chapinero, Cali, Colombia",
    "villacolombia": "Barrio Villacolombia, Cali, Colombia",
    "villa colombia": "Barrio Villacolombia, Cali, Colombia",
    "rafael uribe uribe": "Barrio Rafael Uribe Uribe, Cali, Colombia",
    "siete de agosto": "Barrio Siete de Agosto, Cali, Colombia",
    "7 de agosto": "Barrio Siete de Agosto, Cali, Colombia",

    # Sur
    "melendez": "Barrio Melendez, Cali, Colombia",
    "meléndez": "Barrio Melendez, Cali, Colombia",
    "el ingenio": "Barrio El Ingenio, Cali, Colombia",
    "ingenio": "Barrio El Ingenio, Cali, Colombia",
    "ciudad jardin": "Barrio Ciudad Jardin, Cali, Colombia",
    "ciudad jardín": "Barrio Ciudad Jardin, Cali, Colombia",
    "pance": "Pance, Cali, Colombia",
    "la buitrera": "La Buitrera, Cali, Colombia",
    "mayapan": "Barrio Mayapan, Cali, Colombia",
    "mayapán": "Barrio Mayapan, Cali, Colombia",
    "capri": "Barrio Capri, Cali, Colombia",
    "el limonar": "Barrio El Limonar, Cali, Colombia",
    "limonar": "Barrio El Limonar, Cali, Colombia",
    "la hacienda": "Barrio La Hacienda, Cali, Colombia",
    "camino real": "Barrio Camino Real, Cali, Colombia",
    "cuarto de legua": "Barrio Cuarto de Legua, Cali, Colombia",
    "santa anita": "Barrio Santa Anita, Cali, Colombia",
    "la selva": "Barrio La Selva, Cali, Colombia",
    "bochalema": "Barrio Bochalema, Cali, Colombia",
    "valle del lili": "Barrio Valle del Lili, Cali, Colombia",
    "lili": "Barrio Valle del Lili, Cali, Colombia",
    "caney": "Barrio El Caney, Cali, Colombia",
    "el caney": "Barrio El Caney, Cali, Colombia",
    "ciudad pacifica": "Barrio Ciudad Pacifica, Cali, Colombia",
    "ciudad pacífica": "Barrio Ciudad Pacifica, Cali, Colombia",

    # Suroriente
    "republica de israel": "Barrio Republica de Israel, Cali, Colombia",
    "república de israel": "Barrio Republica de Israel, Cali, Colombia",
    "mariano ramos": "Barrio Mariano Ramos, Cali, Colombia",
    "morichal de comfandi": "Barrio Morichal de Comfandi, Cali, Colombia",
    "brisas del limonar": "Barrio Brisas del Limonar, Cali, Colombia",
    "el refugio": "Barrio El Refugio, Cali, Colombia",
    "caldas": "Barrio Caldas, Cali, Colombia",
    "los cambulos": "Barrio Los Cambulos, Cali, Colombia",
    "los cámbulos": "Barrio Los Cambulos, Cali, Colombia",
}


RUTAS_FALLBACK = {
    ("centro", "univalle"): {
        "puntos": [
            [3.4516, -76.5320],
            [3.4380, -76.5325],
            [3.4215, -76.5330],
            [3.4050, -76.5340],
            [3.3755, -76.5338],
        ],
        "distancia_total": 8.5,
        "duracion_estimada": 20,
    },
    ("univalle", "centro"): {
        "puntos": [
            [3.3755, -76.5338],
            [3.4050, -76.5340],
            [3.4215, -76.5330],
            [3.4380, -76.5325],
            [3.4516, -76.5320],
        ],
        "distancia_total": 8.5,
        "duracion_estimada": 20,
    },
    ("las ceibas", "valle grande"): {
        "puntos": [
            [3.4560, -76.4910],
            [3.4540, -76.4800],
            [3.4520, -76.4680],
            [3.4490, -76.4550],
            [3.4460, -76.4420],
        ],
        "distancia_total": 6.2,
        "duracion_estimada": 15,
    },
    ("valle grande", "las ceibas"): {
        "puntos": [
            [3.4460, -76.4420],
            [3.4490, -76.4550],
            [3.4520, -76.4680],
            [3.4540, -76.4800],
            [3.4560, -76.4910],
        ],
        "distancia_total": 6.2,
        "duracion_estimada": 15,
    },
    ("terminal", "san antonio"): {
        "puntos": [
            [3.4635, -76.5202],
            [3.4550, -76.5245],
            [3.4500, -76.5320],
            [3.4470, -76.5410],
        ],
        "distancia_total": 4.8,
        "duracion_estimada": 14,
    },
    ("chipichape", "centro"): {
        "puntos": [
            [3.4765, -76.5288],
            [3.4680, -76.5295],
            [3.4600, -76.5305],
            [3.4516, -76.5320],
        ],
        "distancia_total": 3.8,
        "duracion_estimada": 12,
    },
    ("melendez", "centro"): {
        "puntos": [
            [3.3765, -76.5360],
            [3.3970, -76.5355],
            [3.4215, -76.5330],
            [3.4516, -76.5320],
        ],
        "distancia_total": 8.1,
        "duracion_estimada": 22,
    },
    ("centro", "ciudad jardin"): {
        "puntos": [
            [3.4516, -76.5320],
            [3.4215, -76.5330],
            [3.3950, -76.5350],
            [3.3675, -76.5310],
        ],
        "distancia_total": 10.2,
        "duracion_estimada": 25,
    },
}


def quitar_tildes(texto):
    texto_normalizado = unicodedata.normalize("NFD", texto)
    return "".join(
        caracter
        for caracter in texto_normalizado
        if unicodedata.category(caracter) != "Mn"
    )


def normalizar_texto(texto):
    if not texto:
        return ""

    texto = quitar_tildes(texto)
    return " ".join(texto.lower().strip().split())


def obtener_nombre_lugar(lugar):
    lugar_normalizado = normalizar_texto(lugar)

    if lugar_normalizado in LUGARES_CALI:
        return LUGARES_CALI[lugar_normalizado]

    return f"{lugar}, Cali, Colombia"


def cargar_comunas():
    if not COMUNAS_PATH.exists():
        raise FileNotFoundError(f"No existe el archivo de comunas: {COMUNAS_PATH}")

    with COMUNAS_PATH.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def geocodificar_lugar(lugar):
    if not ORS_API_KEY:
        raise RuntimeError("ORS_API_KEY no configurada en backend/.env")

    url = "https://api.openrouteservice.org/geocode/search"

    params = {
        "api_key": ORS_API_KEY,
        "text": obtener_nombre_lugar(lugar),
        "size": 1,
        "boundary.country": "CO",
        "boundary.rect.min_lon": CALI_BOUNDS["min_lon"],
        "boundary.rect.min_lat": CALI_BOUNDS["min_lat"],
        "boundary.rect.max_lon": CALI_BOUNDS["max_lon"],
        "boundary.rect.max_lat": CALI_BOUNDS["max_lat"],
    }

    response = requests.get(url, params=params, timeout=15)

    if response.status_code != 200:
        raise RuntimeError(
            f"Error geocodificando '{lugar}'. "
            f"Status: {response.status_code}. Respuesta: {response.text}"
        )

    data = response.json()
    features = data.get("features", [])

    if not features:
        raise RuntimeError(f"No se pudo geocodificar el lugar: {lugar}")

    # OpenRouteService usa [lng, lat]
    return features[0]["geometry"]["coordinates"]


def solicitar_ruta_openrouteservice(origen, destino):
    origen_coords = geocodificar_lugar(origen)
    destino_coords = geocodificar_lugar(destino)

    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json",
    }

    body = {
        "coordinates": [
            origen_coords,
            destino_coords,
        ]
    }

    response = requests.post(url, json=body, headers=headers, timeout=20)

    if response.status_code != 200:
        error_msg = f"Error en OpenRouteService. Status: {response.status_code}. Respuesta: {response.text}"
        print(f"OpenRouteService falló: {error_msg}")
        raise RuntimeError(error_msg)

    data = response.json()
    features = data.get("features", [])

    if not features:
        raise RuntimeError("OpenRouteService no devolvió una ruta válida")

    feature = features[0]
    coordenadas_ors = feature["geometry"]["coordinates"]

    # Convertir de [lng, lat] a [lat, lng] para Leaflet
    puntos = [[lat, lng] for lng, lat in coordenadas_ors]

    segmento = feature["properties"]["segments"][0]
    distancia_km = segmento["distance"] / 1000
    duracion_min = segmento["duration"] / 60

    return {
        "fuente": "openrouteservice",
        "mensaje": "Ruta calculada con OpenRouteService",
        "origen": origen,
        "destino": destino,
        "puntos": puntos,
        "distancia_total": round(distancia_km, 2),
        "duracion_estimada": round(duracion_min, 1),
    }


def calcular_distancia_haversine(punto_a, punto_b):
    lat1, lon1 = punto_a
    lat2, lon2 = punto_b

    radio_tierra_km = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return radio_tierra_km * c


def calcular_centroide(coordenadas):
    if not coordenadas:
        return [3.4516, -76.5320]

    lat = sum(punto[0] for punto in coordenadas) / len(coordenadas)
    lng = sum(punto[1] for punto in coordenadas) / len(coordenadas)

    return [lat, lng]


def encontrar_comuna_por_punto(punto, comunas):
    comuna_mas_cercana = None
    distancia_minima = float("inf")

    for comuna in comunas:
        coordenadas = comuna.get("coordenadas", [])

        if not coordenadas:
            continue

        centroide = calcular_centroide(coordenadas)
        distancia = calcular_distancia_haversine(punto, centroide)

        if distancia < distancia_minima:
            distancia_minima = distancia
            comuna_mas_cercana = comuna

    return comuna_mas_cercana


def crear_tramo(indice, puntos_tramo, comunas):
    if not puntos_tramo or len(puntos_tramo) < 1:
        return None

    inicio = puntos_tramo[0]
    fin = puntos_tramo[-1]

    # Calcular distancia sumando Haversine entre cada par de puntos
    distancia = 0.0
    for i in range(len(puntos_tramo) - 1):
        distancia += calcular_distancia_haversine(puntos_tramo[i], puntos_tramo[i + 1])

    # Punto medio para buscar la comuna
    punto_medio = [
        (inicio[0] + fin[0]) / 2,
        (inicio[1] + fin[1]) / 2,
    ]

    comuna = encontrar_comuna_por_punto(punto_medio, comunas)

    if comuna is None:
        comuna = {
            "nombre": "Zona no identificada",
            "criminalidad": 5,
            "seguridad": 5,
            "vigilancia": 5,
            "iluminacion": 5,
            "flujo_personas": 5,
        }

    return {
        "tramo": indice,
        "inicio": inicio,
        "fin": fin,
        "puntos": puntos_tramo,
        "distancia": round(distancia, 3),
        "comuna": comuna.get("nombre", "Zona no identificada"),
        "criminalidad": comuna.get("criminalidad", 5),
        "seguridad": comuna.get("seguridad", 5),
        "vigilancia": comuna.get("vigilancia", 5),
        "iluminacion": comuna.get("iluminacion", 5),
        "flujo_personas": comuna.get("flujo_personas", 5),
    }


def dividir_ruta_en_tramos(puntos, comunas, max_tramos=18):
    if len(puntos) < 2:
        return []

    total_puntos = len(puntos)
    num_tramos = min(max_tramos, max(1, total_puntos // 5))
    
    # Calcular cuántos puntos por tramo
    puntos_por_tramo = max(2, total_puntos // num_tramos)

    tramos = []
    indice_tramo = 1

    i = 0
    while i < total_puntos:
        # Determinar el final del tramo
        fin_tramo = min(i + puntos_por_tramo, total_puntos)
        
        # Si es el último tramo, incluir todos los puntos restantes
        if fin_tramo >= total_puntos - 1:
            fin_tramo = total_puntos

        puntos_tramo = puntos[i:fin_tramo]

        if len(puntos_tramo) >= 2:
            tramo = crear_tramo(indice_tramo, puntos_tramo, comunas)
            if tramo:
                tramos.append(tramo)
                indice_tramo += 1

        i = fin_tramo - 1  # Solapar un punto para continuidad

    return tramos


def obtener_ruta_fallback(origen, destino, comunas):
    origen_norm = normalizar_texto(origen)
    destino_norm = normalizar_texto(destino)
    clave = (origen_norm, destino_norm)

    if clave not in RUTAS_FALLBACK:
        clave = ("centro", "univalle")
        mensaje = (
            "No se pudo consultar OpenRouteService y no existe una ruta local "
            "para ese origen/destino. Se usó una ruta interna de ejemplo en Cali."
        )
    else:
        mensaje = (
            "No se pudo consultar OpenRouteService. "
            "Se usó una ruta local aproximada para mantener la demostración."
        )

    datos = RUTAS_FALLBACK[clave]
    puntos = datos["puntos"]

    return {
        "fuente": "fallback_local",
        "mensaje": mensaje,
        "origen": origen,
        "destino": destino,
        "puntos": puntos,
        "distancia_total": datos["distancia_total"],
        "duracion_estimada": datos["duracion_estimada"],
        "tramos": dividir_ruta_en_tramos(puntos, comunas),
    }


def obtener_ruta(origen, destino, comunas=None):
    if not origen or not destino:
        raise ValueError("Origen y destino son obligatorios")

    if comunas is None:
        comunas = cargar_comunas()

    try:
        ruta = solicitar_ruta_openrouteservice(origen, destino)
        ruta["tramos"] = dividir_ruta_en_tramos(ruta["puntos"], comunas)
        return ruta

    except Exception as error:
        print(f"OpenRouteService falló: {error}")
        return obtener_ruta_fallback(origen, destino, comunas)