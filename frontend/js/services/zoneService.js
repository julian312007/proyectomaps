import { API_BASE_URL } from '../config.js';

export function obtenerComunas() {
  return fetch(`${API_BASE_URL}/comunas`)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Error al obtener comunas');
      }
      return response.json();
    });
}