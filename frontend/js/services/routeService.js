import { API_BASE_URL } from '../config.js';

export function obtenerRutaDemo() {
  return fetch(`${API_BASE_URL}/ruta-demo`)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Error al obtener ruta demo');
      }
      return response.json();
    });
}
