import { useCallback, useEffect, useRef, useState } from 'react';
import Ventana from '../componentes/Ventana.jsx';
import Grilla from '../componentes/Grilla.jsx';
import Aviso, { avisoDeError } from '../componentes/Aviso.jsx';
import SelectorReferencia from '../componentes/SelectorReferencia.jsx';
import { ErrorValidacion } from '../modelo/validador.js';
import Notificador from '../servicios/notificador.js';

const TAMANOS = [10, 25, 50, 100];
const PAGINA_VACIA = { elementos: [], total: 0, pagina: 0, tamano: 25, totalPaginas: 1 };
const miles = (n) => n.toLocaleString('es-CO');

/**
 * Caso de uso: Listar en una grilla PAGINADA, con filtro por un parámetro.
 * El servidor solo envía la página visible y el total, así responde igual con miles de registros.
 */
export default function VistaListar({ entidad, onCerrar }) {
  const [indiceFiltro, setIndiceFiltro] = useState(0);
  const [valor, setValor] = useState('');
  const [tamano, setTamano] = useState(25);
  const [resultado, setResultado] = useState(PAGINA_VACIA);
  const [aviso, setAviso] = useState(null);
  const [cargando, setCargando] = useState(false);
  const filtro = entidad.filtros[indiceFiltro];

  // filtro y valor de la última consulta aplicada (la paginación los conserva)
  const aplicada = useRef({ filtro: entidad.filtros[0], valor: '' });
  const estado = useRef({ pagina: 0, tamano: 25 });

  const cargar = useCallback(async (pagina, tam = estado.current.tamano) => {
    const { filtro: f, valor: v } = aplicada.current;
    setAviso(null);
    setCargando(true);
    try {
      let r = await entidad.listar(f.clave, String(v).trim(), pagina, tam);
      if (r.elementos.length === 0 && pagina > 0 && r.total > 0) {
        // la página quedó vacía (p. ej. se eliminó su último registro): ir a la última
        r = await entidad.listar(f.clave, String(v).trim(), r.totalPaginas - 1, tam);
      }
      estado.current = { pagina: r.pagina, tamano: tam };
      setResultado(r);
    } catch (e) {
      setAviso(avisoDeError(e));
    } finally {
      setCargando(false);
    }
  }, [entidad]);

  useEffect(() => { cargar(0); }, [cargar]);

  // Patrón Observer: si cambian los datos, se recarga la misma página con el mismo filtro
  useEffect(() => {
    const cancelaciones = entidad.eventosObservados.map((ev) =>
      Notificador.obtener().suscribir(ev, () => cargar(estado.current.pagina)));
    return () => cancelaciones.forEach((cancelar) => cancelar());
  }, [cargar, entidad]);

  const aplicar = () => {
    try {
      if (filtro.clave && !String(valor).trim()) {
        throw new ErrorValidacion([`Escriba o seleccione un valor para “${filtro.etiqueta}”.`]);
      }
      if (filtro.tipo === 'referencia' && !/^\d+$/.test(String(valor))) {
        throw new ErrorValidacion(['Escriba el nombre o el ID del agente y elíjalo de la lista.']);
      }
      aplicada.current = { filtro, valor };
      cargar(0);
    } catch (e) {
      setAviso(avisoDeError(e));
    }
  };

  const listarTodos = () => {
    setIndiceFiltro(0);
    setValor('');
    aplicada.current = { filtro: entidad.filtros[0], valor: '' };
    cargar(0);
  };

  const cambiarTamano = (t) => {
    setTamano(t);
    cargar(0, t);
  };

  let control = <input aria-label="Valor del filtro" value="" disabled placeholder="Sin filtro" />;
  if (filtro.tipo === 'texto') {
    control = <input aria-label="Valor del filtro" value={valor} onChange={(e) => setValor(e.target.value)} placeholder="Ej. Bogota" />;
  } else if (filtro.tipo === 'opcion') {
    control = (
      <select aria-label="Valor del filtro" value={valor} onChange={(e) => setValor(e.target.value)}>
        <option value="">Seleccione…</option>
        {filtro.opciones.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    );
  } else if (filtro.tipo === 'referencia') {
    control = (
      <SelectorReferencia valor={valor} onCambio={setValor} buscar={entidad.proveedorReferencias}
        placeholder="Escriba nombre o ID del agente" />
    );
  }

  const { elementos, total, pagina, totalPaginas } = resultado;
  const desde = total ? pagina * tamano + 1 : 0;
  const hasta = pagina * tamano + elementos.length;
  const filtroAplicado = aplicada.current.filtro.clave ? ` · filtro ${aplicada.current.filtro.etiqueta.toLowerCase()}` : '';

  return (
    <Ventana titulo={`Listar ${entidad.plural}`} rol={entidad.rol} onCerrar={onCerrar}
      descripcion="Registros en una grilla paginada. Puede filtrar por un parámetro.">
      <form className="filtros" onSubmit={(e) => { e.preventDefault(); aplicar(); }}>
        <label htmlFor="filtro">Filtrar por</label>
        <select id="filtro" value={indiceFiltro} onChange={(e) => { setIndiceFiltro(Number(e.target.value)); setValor(''); }}>
          {entidad.filtros.map((f, i) => <option key={f.etiqueta} value={i}>{f.etiqueta}</option>)}
        </select>
        {control}
        <button type="submit" className="boton boton--primario" disabled={cargando}>Aplicar filtro</button>
        <button type="button" className="boton" onClick={listarTodos} disabled={cargando}>Listar todos</button>
      </form>
      <Aviso aviso={aviso} />
      <p className="nota">Las columnas sombreadas vienen de la otra colección.</p>
      <Grilla columnas={entidad.columnas} filas={elementos} />
      <div className="paginacion">
        <span className="nota" aria-live="polite">
          {cargando ? 'Consultando…' : `Mostrando ${desde}–${hasta} de ${miles(total)} registro(s)${filtroAplicado}`}
        </span>
        <div className="paginacion__controles">
          <label htmlFor="tamano">Filas por página</label>
          <select id="tamano" value={tamano} onChange={(e) => cambiarTamano(Number(e.target.value))}>
            {TAMANOS.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
          <button type="button" className="boton" disabled={cargando || pagina === 0}
            onClick={() => cargar(pagina - 1)}>◀ Anterior</button>
          <span>Página {pagina + 1} de {miles(totalPaginas)}</span>
          <button type="button" className="boton" disabled={cargando || pagina + 1 >= totalPaginas}
            onClick={() => cargar(pagina + 1)}>Siguiente ▶</button>
        </div>
      </div>
    </Ventana>
  );
}
