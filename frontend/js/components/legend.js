export function renderLegend() {
  const container = document.getElementById('legend');
  container.innerHTML = `
    <div class="panel-section">
      <h2>Leyenda</h2>
      <ul class="legend-list">
        <li><span class="legend-color low"></span>Riesgo bajo</li>
        <li><span class="legend-color medium"></span>Riesgo medio</li>
        <li><span class="legend-color high"></span>Riesgo alto</li>
      </ul>
    </div>
  `;
}
