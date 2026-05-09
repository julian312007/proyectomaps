const COLOR_BY_LEVEL = {
  bajo: '#16a34a',
  medio: '#f59e0b',
  alto: '#dc2626',
};

export function drawRoute(map, puntos, nivelesPorTramo) {
  const layers = [];

  for (let index = 0; index < puntos.length - 1; index += 1) {
    const puntoActual = puntos[index];
    const siguientePunto = puntos[index + 1];
    const nivel = nivelesPorTramo[index] || 'medio';
    const color = COLOR_BY_LEVEL[nivel] || COLOR_BY_LEVEL.medio;

    const polyline = L.polyline([
      [puntoActual.lat, puntoActual.lng],
      [siguientePunto.lat, siguientePunto.lng],
    ], {
      color,
      weight: 5,
      opacity: 0.8,
    }).addTo(map);

    layers.push(polyline);
  }

  return layers;
}
