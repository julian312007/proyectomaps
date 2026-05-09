import { initializeMap } from './map/map.js';
import { addRiskMarkers } from './map/markers.js';
import { drawRoute } from './map/routeLayer.js';
import { renderSearchPanel, showRouteMessage } from './components/searchPanel.js';
import { renderRiskPanel, updateRiskResult } from './components/riskPanel.js';
import { renderLegend } from './components/legend.js';
import { obtenerZonasRiesgo, calcularRiesgoRuta } from './services/riskService.js';
import { obtenerRutaDemo } from './services/routeService.js';

let routeLayers = [];

function obtenerTramosSimulados(ruta) {
  return ruta.puntos.map((punto) => ({
    tramo: punto.tramo,
    criminalidad: 6,
    seguridad: 4,
    distancia: punto.distancia,
  }));
}

document.addEventListener('DOMContentLoaded', () => {
  const map = initializeMap();

  renderSearchPanel(handleRouteCalculation);
  renderRiskPanel();
  renderLegend();

  obtenerZonasRiesgo()
    .then((zonas) => {
      addRiskMarkers(map, zonas);
    })
    .catch((error) => {
      console.error(error);
      showRouteMessage('No fue posible cargar las zonas de riesgo.', true);
    });

  obtenerRutaDemo()
    .then((rutaDemo) => {
      const tramos = obtenerTramosSimulados(rutaDemo);
      calcularRiesgoRuta(tramos)
        .then((resultado) => {
          updateRiskResult(resultado.riesgo_final, resultado.nivel_final);
          const niveles = resultado.tramos.map((tramo) => tramo.nivel);
          routeLayers = drawRoute(map, rutaDemo.puntos, niveles);
          showRouteMessage('Ruta demo cargada y riesgo calculado.', false);
        })
        .catch((error) => {
          console.error(error);
          showRouteMessage('Error al calcular riesgo de ruta demo.', true);
        });
    })
    .catch((error) => {
      console.error(error);
      showRouteMessage('No fue posible cargar la ruta demo.', true);
    });
});

function handleRouteCalculation(origin, destination) {
  const rutaDemo = {
    puntos: [
      { tramo: 1, criminalidad: 6, seguridad: 4, distancia: 0.6 },
      { tramo: 2, criminalidad: 5, seguridad: 5, distancia: 0.5 },
      { tramo: 3, criminalidad: 7, seguridad: 3, distancia: 0.7 },
    ],
  };

  calcularRiesgoRuta(rutaDemo.puntos)
    .then((resultado) => {
      updateRiskResult(resultado.riesgo_final, resultado.nivel_final);
      showRouteMessage(`Ruta simulada: ${origin} → ${destination}.`, false);
    })
    .catch((error) => {
      console.error(error);
      showRouteMessage('Error al simular el cálculo de ruta.', true);
    });
}
