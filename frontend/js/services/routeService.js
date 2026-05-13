import { API_BASE_URL } from '../config.js';

export async function obtenerRuta(origen, destino) {
  const query = new URLSearchParams({ origen, destino });

  const response = await fetch(`${API_BASE_URL}/ruta?${query.toString()}`);

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detalle || data.error || 'Error al obtener ruta');
  }

  return data;
}

export function obtenerRutaDemo() {
  return fetch(`${API_BASE_URL}/ruta-demo`)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Error al obtener ruta demo');
      }
      return response.json();
    });
}
