export function renderRiskPanel() {
  const container = document.getElementById('risk-panel');
  container.innerHTML = `
    <div class="panel-section">
      <h2>Resultado de riesgo</h2>
      <p id="risk-result">Ingresa origen y destino, luego presiona Calcular ruta.</p>
      <p id="risk-level" class="risk-level"></p>
      <p id="risk-alert" class="risk-alert"></p>
      <div id="route-details" style="display: none;">
        <p><strong>Origen:</strong> <span id="route-origin"></span></p>
        <p><strong>Destino:</strong> <span id="route-destino"></span></p>
        <p><strong>Distancia total:</strong> <span id="route-distancia"></span> km</p>
        <p><strong>Duración estimada:</strong> <span id="route-duracion"></span> min</p>
        <p><strong>Modelo usado:</strong> <span id="route-modelo"></span></p>
        <p><strong>Riesgo inicial:</strong> <span id="route-riesgo-inicial"></span></p>
        <p><strong>Riesgo final:</strong> <span id="route-riesgo-final"></span></p>
        <p><strong>Nivel final:</strong> <span id="route-nivel-final"></span></p>
        <h3>Tramos</h3>
        <table id="tramos-table" border="1" style="width: 100%; border-collapse: collapse;">
          <thead>
            <tr>
              <th>Tramo</th>
              <th>Comuna</th>
              <th>Distancia (km)</th>
              <th>Derivada</th>
              <th>Riesgo Acumulado</th>
              <th>Nivel</th>
            </tr>
          </thead>
          <tbody id="tramos-body"></tbody>
        </table>
      </div>
    </div>
  `;
}

export function updateRiskResult({ ruta, resultado }) {
  const resultElement = document.getElementById('risk-result');
  const levelElement = document.getElementById('risk-level');
  const alertElement = document.getElementById('risk-alert');
  const detailsElement = document.getElementById('route-details');
  
  // Mostrar fuente de la ruta
  const fuente = ruta.fuente || 'desconocida';
  const mensajeFuente = fuente === 'openrouteservice' 
    ? '(Ruta real por OpenRouteService)'
    : '(Ruta local aproximada)';

  if (resultElement) {
    resultElement.textContent = `Riesgo final estimado: ${resultado.riesgo_final}`;
  }

  if (levelElement) {
    levelElement.textContent = `Nivel final: ${resultado.nivel_final}`;
  }

  if (alertElement) {
    const mensaje = {
      bajo: 'Ruta con riesgo bajo.',
      medio: 'Ruta con riesgo medio. Mantente atento.',
      alto: 'Ruta con riesgo alto. Considera otra ruta.',
      critico: 'Ruta con riesgo crítico. Se recomienda evitar esta ruta.',
    }[resultado.nivel_final] || 'Riesgo de ruta calculado';

    alertElement.textContent = mensaje;
  }

  if (detailsElement) {
    detailsElement.style.display = 'block';
    document.getElementById('route-origin').textContent = ruta.origen + ' ' + mensajeFuente;
    document.getElementById('route-destino').textContent = ruta.destino;
    document.getElementById('route-distancia').textContent = ruta.distancia_total.toFixed(2);
    document.getElementById('route-duracion').textContent = ruta.duracion_estimada.toFixed(2);
    document.getElementById('route-modelo').textContent = resultado.modelo_usado;
    document.getElementById('route-riesgo-inicial').textContent = resultado.riesgo_inicial;
    document.getElementById('route-riesgo-final').textContent = resultado.riesgo_final;
    document.getElementById('route-nivel-final').textContent = resultado.nivel_final;

    const tbody = document.getElementById('tramos-body');
    tbody.innerHTML = '';
    resultado.tramos.forEach((tramo) => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${tramo.tramo}</td>
        <td>${tramo.comuna}</td>
        <td>${tramo.distancia.toFixed(2)}</td>
        <td>${tramo.derivada}</td>
        <td>${tramo.riesgo_acumulado}</td>
        <td>${tramo.nivel}</td>
      `;
      tbody.appendChild(row);
    });
  }
}
