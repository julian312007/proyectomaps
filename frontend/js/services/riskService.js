import { API_BASE_URL } from '../config.js';

export async function obtenerZonasRiesgo() {
  const response = await fetch(`${API_BASE_URL}/riesgos`);

  if (!response.ok) {
    throw new Error('Error al cargar zonas de riesgo');
  }

  return response.json();
}

export async function calcularRiesgoRuta(
  tramos,
  riesgoInicial = 1,
  modelo = 'no_lineal'
) {
  const response = await fetch(`${API_BASE_URL}/calcular-riesgo-ruta`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      riesgo_inicial: riesgoInicial,
      modelo,
      tramos,
    }),
  });

  if (!response.ok) {
    const errorBody = await response.json();
    throw new Error(errorBody.error || 'Error al calcular riesgo de ruta');
  }

  return response.json();
}