import { MAP_CONFIG, TILE_LAYER, TILE_ATTRIBUTION } from '../config.js';

export function initializeMap() {
  const map = L.map('map').setView(MAP_CONFIG.center, MAP_CONFIG.zoom);

  L.tileLayer(TILE_LAYER, {
    attribution: TILE_ATTRIBUTION,
  }).addTo(map);

  return map;
}
