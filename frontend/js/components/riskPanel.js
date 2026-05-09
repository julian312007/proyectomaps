export function renderRiskPanel() {
  const container = document.getElementById('risk-panel');
  container.innerHTML = `
    <div class="panel-section">
      <h2>Resultado de riesgo</h2>
      <p id="risk-result">Ingresa origen y destino, luego presiona Calcular ruta.</p>
      <p id="risk-level" class="risk-level"></p>
      <p id="risk-alert" class="risk-alert"></p>
    </div>
  `;
}

export function updateRiskResult(riesgoFinal, nivelFinal) {
  const resultElement = document.getElementById('risk-result');
  const levelElement = document.getElementById('risk-level');
  const alertElement = document.getElementById('risk-alert');

  if (resultElement) {
    resultElement.textContent = `Riesgo final estimado: ${riesgoFinal}`;
  }

  if (levelElement) {
    levelElement.textContent = `Nivel final: ${nivelFinal}`;
  }

  if (alertElement) {
    const mensaje = {
      bajo: 'Ruta con riesgo bajo',
      medio: 'Ruta con riesgo medio',
      alto: 'Ruta con riesgo alto',
    }[nivelFinal] || 'Riesgo de ruta calculado';

    alertElement.textContent = mensaje;
  }
}
