import { initializeMap } from './map/map.js';
import { drawRoute } from './map/routeLayer.js';
import { drawRiskZones } from './map/zonesLayer.js';
import { renderSearchPanel, showRouteMessage } from './components/searchPanel.js';
import { renderRiskPanel, updateRiskResult } from './components/riskPanel.js';
import { renderLegend } from './components/legend.js';
import { obtenerComunas } from './services/zoneService.js';
import { obtenerRuta } from './services/routeService.js';
import { calcularRiesgoRuta } from './services/riskService.js';

let map;

document.addEventListener('DOMContentLoaded', async () => {
  map = initializeMap();

  renderSearchPanel(handleRouteCalculation);
  renderRiskPanel();
  renderLegend();

  try {
    const comunas = await obtenerComunas();
    drawRiskZones(map, comunas);
  } catch (error) {
    console.error(error);
    showRouteMessage('No fue posible cargar las comunas de Cali.', true);
  }
});

async function handleRouteCalculation(origin, destination) {
  try {
    showRouteMessage('Calculando ruta real...', false);

    const ruta = await obtenerRuta(origin, destination);

    const resultadoRiesgo = await calcularRiesgoRuta(
      ruta.tramos,
      1,
      'no_lineal'
    );

    drawRoute(map, ruta, resultadoRiesgo);

    updateRiskResult({
      ruta,
      resultado: resultadoRiesgo,
    });

    showRouteMessage('Ruta calculada correctamente.', false);
  } catch (error) {
    console.error(error);
    showRouteMessage('Error al obtener la ruta.', true);
  }
}
