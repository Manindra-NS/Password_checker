import { initAurora } from './aurora.js';

const auroraEl = document.getElementById('aurora-bg');
if (auroraEl) {
  initAurora(auroraEl, {
    colorStops: ['#7cff67', '#B497CF', '#5227FF'],
    amplitude: 1.0,
    blend: 0.5,
    speed: 1
  });
}