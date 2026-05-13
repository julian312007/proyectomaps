# PROYECTOMAPS

Proyecto web para visualizar riesgo urbano con Flask, JavaScript puro y Leaflet.

## Estructura del proyecto

```
PROYECTOMAPS/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── services/
│   │   ├── math_service.py
│   │   ├── route_service.py
│   │   └── risk_service.py
│   └── data/
│       ├── riesgos.json
│       └── ruta_demo.json
│
├── frontend/
│   ├── index.html
│   ├── styles/
│   │   └── styles.css
│   └── js/
│       ├── app.js
│       ├── config.js
│       ├── map/
│       │   ├── map.js
│       │   ├── markers.js
│       │   └── routeLayer.js
│       ├── services/
│       │   ├── riskService.js
│       │   └── routeService.js
│       ├── components/
│       │   ├── legend.js
│       │   ├── riskPanel.js
│       │   └── searchPanel.js
│       └── utils/
│           └── riskCalculator.js
│
├── .gitignore
└── README.md
```

## Backend disponible

- `GET /api/health` → verifica que el backend está funcionando.
- `GET /api/riesgos` → devuelve las zonas de riesgo con cálculo de `riesgo` y `nivel`.
- `GET /api/ruta-demo` → devuelve una ruta simulada con puntos y `distancia_total`.
- `POST /api/calcular-riesgo-ruta` → recibe tramos y devuelve riesgo acumulado por tramo.

## Datos

- `backend/data/riesgos.json` contiene las zonas de ejemplo.
- `backend/data/ruta_demo.json` contiene los puntos de la ruta demo.

## Cómo ejecutar el proyecto

1. Crea un archivo `.env` en la raíz del proyecto con tu API key de OpenRouteService:

   ```
   ORS_API_KEY=tu_api_key_aqui
   ```

   Obtén tu API key gratuita en: https://openrouteservice.org/

2. Activa el entorno virtual:

   PowerShell:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   CMD:
   ```cmd
   .venv\Scripts\activate.bat
   ```

   Si no tienes el entorno virtual creado:
   ```powershell
   python -m venv .venv
   ```

3. Instala dependencias:

   ```powershell
   python -m pip install -r backend\requirements.txt
   ```

4. Ejecuta el backend:

   ```powershell
   python backend\app.py
   ```

5. Abre el navegador en:

   ```text
   http://127.0.0.1:5000/
   ```

## Qué se logra en esta etapa

- Frontend organizado con Leaflet y módulos JavaScript.
- Backend Flask con APIs para zonas de riesgo y ruta demo.
- Conexión entre frontend y backend mediante fetch.
- Mapa con marcadores de riesgo y ruta demo dibujada.
- Cálculo de riesgo acumulado en el backend con el modelo discreto.

## Recomendaciones

- No usar React ni base de datos todavía.
- El flujo actual está preparado para agregar rutas reales y visualización avanzada en la siguiente etapa.
