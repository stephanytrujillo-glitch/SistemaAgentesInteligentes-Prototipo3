/** Formato de valores para mostrarlos al usuario. */
export function formatear(tipo, valor) {
  if (tipo === 'referencia' && (valor === null || valor === undefined)) return 'Sin asignar';
  if (valor === null || valor === undefined || valor === '') return '—';
  if (tipo === 'booleano') return valor ? 'Sí' : 'No';
  if (tipo === 'fecha') return String(valor).replace('T', ' ').slice(0, 16);
  if (tipo === 'decimal') return Number(valor).toFixed(2);
  return String(valor);
}
