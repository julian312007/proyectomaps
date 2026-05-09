const LEVEL_COLORS = {
  bajo: '#16a34a',
  medio: '#f59e0b',
  alto: '#dc2626',
};

export function addRiskMarkers(map, zones) {
  zones.forEach((zone) => {
    const color = LEVEL_COLORS[zone.nivel] || LEVEL_COLORS.medio;
    const marker = L.circleMarker([zone.lat, zone.lng], {
      radius: 8,
      fillColor: color,
      color: '#ffffff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.9,
    }).addTo(map);

    const popupContent = `
      <strong>${zone.nombre}</strong><br>
      Criminalidad: ${zone.criminalidad}<br>
      Seguridad: ${zone.seguridad}<br>
      Riesgo: ${zone.riesgo}<br>
      Nivel: ${zone.nivel}<br>
      ${zone.descripcion}
    `;

    marker.bindPopup(popupContent);
  });
}
