import { useState } from 'react';
import Ventana from '../componentes/Ventana.jsx';
import Buscador from '../componentes/Buscador.jsx';
import Ficha from '../componentes/Ficha.jsx';
import Aviso, { avisoDeError } from '../componentes/Aviso.jsx';

/** Caso de uso: Eliminar. Búsqueda previa y se muestra TODA la información antes de borrar. */
export default function VistaEliminar({ entidad, onCerrar }) {
  const [objeto, setObjeto] = useState(null);
  const [aviso, setAviso] = useState(null);
  const [eliminando, setEliminando] = useState(false);

  const eliminar = async () => {
    const llave = objeto[entidad.servicio.llave];
    const pregunta = `¿Eliminar el ${entidad.nombre} “${objeto.nombre}” (ID ${llave})?\n${entidad.avisoEliminar}\nEsta acción no se puede deshacer.`;
    if (!window.confirm(pregunta)) return;
    try {
      setEliminando(true);
      const mensaje = await entidad.servicio.eliminar(llave);
      setObjeto(null);
      setAviso({ tipo: 'exito', texto: mensaje });
    } catch (e) {
      setAviso(avisoDeError(e));
    } finally {
      setEliminando(false);
    }
  };

  return (
    <Ventana titulo={`Eliminar ${entidad.nombre}`} rol={entidad.rol} onCerrar={onCerrar}
      descripcion="Primero busque el registro y revise toda su información.">
      <Buscador servicio={entidad.servicio}
        onInicio={() => { setObjeto(null); setAviso(null); }}
        onEncontrado={setObjeto}
        onError={(e) => setAviso(avisoDeError(e))} />
      <Aviso aviso={aviso} />
      <Ficha campos={entidad.campos} objeto={objeto} titulo="Registro a eliminar" />
      {entidad.avisoEliminar && objeto && <p className="nota">{entidad.avisoEliminar}</p>}
      <div className="acciones">
        <button type="button" className="boton boton--peligro" onClick={eliminar} disabled={!objeto || eliminando}>
          {eliminando ? 'Eliminando…' : 'Eliminar'}
        </button>
      </div>
    </Ventana>
  );
}
