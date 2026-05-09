import { API_BASE_URL } from '../config.js';

export function obtenerZonasRiesgo() {
  return fetch(`${API_BASE_URL}/riesgos`)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Error al cargar zonas de riesgo');
      }
      return response.json();
    });
}

export function calcularRiesgoRuta(tramos) {
  return fetch(`${API_BASE_URL}/calcular-riesgo-ruta`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      riesgo_inicial: 1,
      tramos,
    }),
  }).then((response) => {
    if (!response.ok) {
      return response.json().then((errorBody) => {
        throw new Error(errorBody.error || 'Error al calcular riesgo de ruta');
      });
    }
    return response.json();
  });
}
