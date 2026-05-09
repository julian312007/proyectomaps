export function renderSearchPanel(onCalculateRoute) {
  const container = document.getElementById('search-panel');
  container.innerHTML = `
    <div class="panel-section">
      <h2>Buscar ruta</h2>
      <form id="route-form" class="route-form">
        <label class="field-group">
          <span>Origen</span>
          <input type="text" name="origin" placeholder="Ej. Avenida Central" />
        </label>

        <label class="field-group">
          <span>Destino</span>
          <input type="text" name="destination" placeholder="Ej. Plaza Mayor" />
        </label>

        <button type="submit" class="button-action">Calcular ruta</button>
        <p id="route-message" class="form-message"></p>
      </form>
    </div>
  `;

  const form = container.querySelector('#route-form');
  const messageElement = container.querySelector('#route-message');

  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const origin = form.origin.value.trim();
    const destination = form.destination.value.trim();

    if (!origin || !destination) {
      messageElement.textContent = 'Por favor ingresa origen y destino.';
      messageElement.classList.add('error');
      return;
    }

    messageElement.textContent = '';
    messageElement.classList.remove('error');
    onCalculateRoute(origin, destination);
  });
}

export function showRouteMessage(message, isError = false) {
  const messageElement = document.getElementById('route-message');
  if (messageElement) {
    messageElement.textContent = message;
    messageElement.classList.toggle('error', isError);
  }
}
