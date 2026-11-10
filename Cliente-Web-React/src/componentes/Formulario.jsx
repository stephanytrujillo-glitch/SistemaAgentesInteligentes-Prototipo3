import SelectorReferencia from './SelectorReferencia.jsx';

/** Formulario generado a partir de la definición de campos de una clase. */
function ahora() {
  const d = new Date();
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
  return d.toISOString().slice(0, 16);
}

export default function Formulario({ campos, valores, onCambio, bloqueados = [], buscarReferencias, mostrarAyuda = true }) {
  const cambiar = (clave, valor) => onCambio({ ...valores, [clave]: valor });

  return (
    <div className="formulario">
      {campos.map((c) => {
        const id = `campo-${c.clave}`;
        const deshabilitado = bloqueados.includes(c.clave);
        let control;
        if (c.tipo === 'booleano') {
          control = (
            <label className="interruptor">
              <input id={id} type="checkbox" checked={Boolean(valores[c.clave])}
                disabled={deshabilitado} onChange={(e) => cambiar(c.clave, e.target.checked)} />
              <span>{valores[c.clave] ? 'Sí' : 'No'}</span>
            </label>
          );
        } else if (c.tipo === 'opcion') {
          control = (
            <select id={id} value={valores[c.clave]} disabled={deshabilitado}
              onChange={(e) => cambiar(c.clave, e.target.value)}>
              <option value="">Seleccione…</option>
              {c.opciones.map((o) => <option key={o} value={o}>{o}</option>)}
            </select>
          );
        } else if (c.tipo === 'referencia') {
          control = (
            <SelectorReferencia id={id} valor={valores[c.clave]} deshabilitado={deshabilitado}
              buscar={buscarReferencias ?? (async () => [])} onCambio={(v) => cambiar(c.clave, v)} />
          );
        } else if (c.tipo === 'fecha') {
          control = (
            <div className="fila-control">
              <input id={id} type="datetime-local" value={valores[c.clave]} disabled={deshabilitado}
                onChange={(e) => cambiar(c.clave, e.target.value)} />
              <button type="button" className="boton boton--sutil" disabled={deshabilitado}
                onClick={() => cambiar(c.clave, ahora())}>Ahora</button>
            </div>
          );
        } else {
          control = (
            <input id={id} type="text" value={valores[c.clave]} disabled={deshabilitado}
              inputMode={c.tipo === 'entero' ? 'numeric' : c.tipo === 'decimal' ? 'decimal' : undefined}
              maxLength={c.maxLargo} onChange={(e) => cambiar(c.clave, e.target.value)} />
          );
        }
        return (
          <div className="campo" key={c.clave}>
            <label htmlFor={id}>
              {c.etiqueta}{c.obligatorio && <span className="obligatorio" aria-hidden="true"> *</span>}
            </label>
            {control}
            {mostrarAyuda && c.ayuda && <small>{c.ayuda}</small>}
          </div>
        );
      })}
      <p className="nota">* Campo obligatorio</p>
    </div>
  );
}
