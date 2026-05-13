export function drawRiskZones(map, comunas) {
  comunas.forEach((comuna) => {
    const color = getColorByNivel(comuna.nivel);
    L.polygon(comuna.coordenadas, {
      color: color,
      fillColor: color,
      fillOpacity: 0.5,
      weight: 2,
    })
      .addTo(map)
      .bindPopup(`<b>${comuna.nombre}</b><br>Riesgo: ${comuna.riesgo_final}<br>Nivel: ${comuna.nivel}`);
  });
}

function getColorByNivel(nivel) {
  switch (nivel) {
    case 'bajo':
      return 'green';
    case 'medio':
      return 'yellow';
    case 'alto':
      return 'orange';
    case 'critico':
      return 'red';
    default:
      return 'gray';
  }
}