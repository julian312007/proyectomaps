const COLOR_BY_LEVEL = {
  bajo: '#16a34a',
  medio: '#f59e0b',
  alto: '#dc2626',
  critico: '#7f1d1d',
};

let routeLayers = [];
let baselineLayer = null;

export function clearRoute() {
  routeLayers.forEach(layer => {
    layer.remove();
  });
  routeLayers = [];
  
  if (baselineLayer) {
    baselineLayer.remove();
    baselineLayer = null;
  }
}

export function drawRoute(map, ruta, resultadoRiesgo) {
  clearRoute();

  // Dibujar línea base azul de toda la ruta
  if (ruta.puntos && ruta.puntos.length > 1) {
    baselineLayer = L.polyline(ruta.puntos, {
      color: '#2563eb',
      weight: 3,
      opacity: 0.4,
    }).addTo(map);
    routeLayers.push(baselineLayer);
  }

  // Dibujar cada tramo con colores según riesgo
  resultadoRiesgo.tramos.forEach((tramo) => {
    const color = COLOR_BY_LEVEL[tramo.nivel] || COLOR_BY_LEVEL.medio;
    
    // Usar puntos del tramo si están disponibles, si no, usar inicio/fin
    const puntosTramo = tramo.puntos && tramo.puntos.length > 0 
      ? tramo.puntos 
      : [tramo.inicio, tramo.fin];
    
    const polyline = L.polyline(puntosTramo, {
      color,
      weight: 7,
      opacity: 0.95,
    }).addTo(map);

    const popupContent = `
      <div style="font-size: 12px; min-width: 200px;">
        <b>Tramo ${tramo.tramo}</b><br/>
        <strong>Comuna:</strong> ${tramo.comuna}<br/>
        <strong>Distancia:</strong> ${tramo.distancia.toFixed(3)} km<br/>
        <strong>Derivada:</strong> ${tramo.derivada}<br/>
        <strong>Riesgo acumulado:</strong> ${tramo.riesgo_acumulado}<br/>
        <strong>Nivel:</strong> <span style="color: ${color}; font-weight: bold;">${tramo.nivel.toUpperCase()}</span>
      </div>
    `;

    polyline.bindPopup(popupContent);

    routeLayers.push(polyline);
  });

  // FitBounds con todos los puntos de la ruta
  if (ruta.puntos && ruta.puntos.length > 1) {
    const routePolyline = L.polyline(ruta.puntos);
    map.fitBounds(routePolyline.getBounds(), { padding: [40, 40] });
  }

  return routeLayers;
}
