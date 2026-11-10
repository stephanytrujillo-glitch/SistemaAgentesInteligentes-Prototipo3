/** Validación y conversión de los datos del formulario antes de enviarlos al servidor. */
export class ErrorValidacion extends Error {
  constructor(errores) {
    super(errores.join('\n'));
    this.errores = errores;
  }
}

export function valoresVacios(campos) {
  return Object.fromEntries(campos.map((c) => [c.clave, c.tipo === 'booleano' ? false : '']));
}

/** Convierte un objeto del servidor a los valores que usa el formulario. */
export function valoresDesdeObjeto(campos, objeto) {
  return Object.fromEntries(campos.map((c) => {
    const v = objeto[c.clave];
    if (c.tipo === 'booleano') return [c.clave, Boolean(v)];
    if (v === null || v === undefined) return [c.clave, ''];
    if (c.tipo === 'fecha') return [c.clave, String(v).slice(0, 16)];
    return [c.clave, String(v)];
  }));
}

export function validar(campos, valores, incluirLlave = true) {
  const errores = [];
  const datos = {};

  for (const c of campos) {
    if (c.esLlave && !incluirLlave) continue;
    const valor = valores[c.clave];
    const nombre = c.etiqueta;

    if (c.tipo === 'booleano') {
      datos[c.clave] = Boolean(valor);
      continue;
    }
    const texto = valor === null || valor === undefined ? '' : String(valor).trim();
    if (texto === '') {
      if (c.obligatorio) errores.push(`${nombre} es obligatorio.`);
      datos[c.clave] = null;
      continue;
    }

    if (c.tipo === 'entero' || c.tipo === 'decimal' || c.tipo === 'referencia') {
      const numero = Number(texto.replace(',', '.'));
      const esEntero = c.tipo !== 'decimal';
      if (Number.isNaN(numero) || (esEntero && !Number.isInteger(numero))) {
        errores.push(c.tipo === 'referencia'
          ? `${nombre}: escriba el nombre o el ID y elija un agente de la lista.`
          : `${nombre} debe ser ${esEntero ? 'un número entero' : 'un número'}.`);
        continue;
      }
      if (c.minimo !== undefined) {
        if (c.minimoExclusivo && numero <= c.minimo) { errores.push(`${nombre} debe ser mayor que ${c.minimo}.`); continue; }
        if (!c.minimoExclusivo && numero < c.minimo) { errores.push(`${nombre} debe ser mayor o igual a ${c.minimo}.`); continue; }
      }
      if (c.maximo !== undefined && numero > c.maximo) { errores.push(`${nombre} debe ser menor o igual a ${c.maximo}.`); continue; }
      datos[c.clave] = numero;
    } else if (c.tipo === 'texto') {
      if (c.minLargo && texto.length < c.minLargo) { errores.push(`${nombre} debe tener al menos ${c.minLargo} caracteres.`); continue; }
      if (c.maxLargo && texto.length > c.maxLargo) { errores.push(`${nombre} admite máximo ${c.maxLargo} caracteres.`); continue; }
      if (c.patron && !c.patron.test(texto)) { errores.push(`${nombre} solo admite letras, números, espacios, punto, guion y guion bajo.`); continue; }
      datos[c.clave] = texto;
    } else if (c.tipo === 'fecha') {
      const fecha = new Date(texto);
      if (Number.isNaN(fecha.getTime())) { errores.push(`${nombre} no es una fecha válida.`); continue; }
      if (fecha > new Date()) { errores.push(`${nombre} no puede ser una fecha futura.`); continue; }
      datos[c.clave] = texto.length === 16 ? `${texto}:00` : texto.slice(0, 19);
    } else if (c.tipo === 'opcion') {
      if (!c.opciones.includes(texto)) { errores.push(`${nombre} debe ser uno de: ${c.opciones.join(', ')}.`); continue; }
      datos[c.clave] = texto;
    }
  }

  if (datos.origen && datos.destino && datos.origen.toLowerCase() === datos.destino.toLowerCase()) {
    errores.push('El origen y el destino deben ser diferentes.');
  }
  if (errores.length) throw new ErrorValidacion(errores);
  return datos;
}
