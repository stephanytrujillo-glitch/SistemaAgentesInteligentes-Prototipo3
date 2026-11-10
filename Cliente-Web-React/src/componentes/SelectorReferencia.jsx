import { useCallback, useEffect, useId, useRef, useState } from 'react';
import Notificador, { AGENTE_INTELIGENTE } from '../servicios/notificador.js';

const etiqueta = (o) => `${o.id} · ${o.nombre}`;

/**
 * Selector de agente inteligente que BUSCA en el servidor mientras se escribe.
 * No carga todos los agentes (con miles sería lento): pide máximo 20 coincidencias
 * por nombre o por ID. `valor` es el ID como texto ('' = sin asignar).
 */
export default function SelectorReferencia({ id, valor, onCambio, buscar, deshabilitado,
  placeholder = 'Sin asignar · escriba nombre o ID' }) {
  const [texto, setTexto] = useState('');
  const [opciones, setOpciones] = useState([]);
  const listaId = useId();
  const textoActual = useRef('');
  textoActual.current = texto;

  const resolver = useCallback((t, lista = opciones) => {
    const limpio = t.trim();
    if (!limpio) return '';
    const elegida = lista.find((o) => etiqueta(o) === limpio);
    if (elegida) return String(elegida.id);
    const numero = limpio.match(/^(\d+)/);
    return numero ? numero[1] : limpio; // texto sin ID: la validación pide elegir de la lista
  }, [opciones]);

  const consultar = useCallback(async (t) => {
    const numero = t.trim().match(/^(\d+)\s*·/);
    try {
      const r = await buscar(numero ? numero[1] : t.trim());
      setOpciones(r);
      return r;
    } catch {
      setOpciones([]);
      return [];
    }
  }, [buscar]);

  // búsqueda con espera de 300 ms tras la última tecla
  useEffect(() => {
    const espera = setTimeout(() => consultar(texto), 300);
    return () => clearTimeout(espera);
  }, [texto, consultar]);

  // Observer: si cambian los agentes inteligentes, se repite la búsqueda
  useEffect(() => Notificador.obtener().suscribir(AGENTE_INTELIGENTE, () => consultar(textoActual.current)), [consultar]);

  // si el valor cambia desde afuera (cargar un objeto, limpiar), se muestra "id · nombre"
  useEffect(() => {
    if (String(valor ?? '') === resolver(textoActual.current)) return;
    if (!valor) { setTexto(''); return; }
    setTexto(String(valor));
    consultar(String(valor)).then((r) => {
      const o = r.find((x) => String(x.id) === String(valor));
      if (o) setTexto(etiqueta(o));
    });
  }, [valor]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <>
      <input id={id} list={listaId} value={texto} disabled={deshabilitado} placeholder={placeholder}
        autoComplete="off"
        onChange={(e) => { setTexto(e.target.value); onCambio(resolver(e.target.value)); }} />
      <datalist id={listaId}>
        {opciones.map((o) => <option key={o.id} value={etiqueta(o)} />)}
      </datalist>
    </>
  );
}
