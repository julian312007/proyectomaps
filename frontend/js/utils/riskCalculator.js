export const RISK_COEFFICIENTS = {
  a: 0.5,
  b: 0.3,
};

export function calculateRisk(criminalidad, seguridad) {
  const risk = RISK_COEFFICIENTS.a * criminalidad - RISK_COEFFICIENTS.b * seguridad;
  return Number(risk.toFixed(2));
}

export function getRiskLevel(risk) {
  if (risk < 1) {
    return 'Bajo';
  }

  if (risk < 2) {
    return 'Medio';
  }

  return 'Alto';
}
