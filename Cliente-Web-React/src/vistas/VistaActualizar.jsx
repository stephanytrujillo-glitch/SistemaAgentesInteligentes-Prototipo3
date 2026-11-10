import { useState } from 'react';
import Ventana from '../componentes/Ventana.jsx';
import Buscador from '../componentes/Buscador.jsx';
import Ficha from '../componentes/Ficha.jsx';
import Formulario from '../componentes/Formulario.jsx';
import Aviso, { avisoDeError } from '../componentes/Aviso.jsx';
import { validar, valoresDesdeObjeto, valoresVacios } from '../modelo/validador.js';

/** Caso de uso: Actualizar uno o varios atributos de un objeto previamente buscado. */
export default function VistaActualizar({ entidad, onCerrar }) {
  const [objeto, setObjeto] = useState(null);
  const [valores, setValores] = useState(() => valoresVacios(entidad.campos));
  const [aviso, setAviso] = useState(null);
  const [guardando, setGuardando] = useState(false);
  const llave = entidad.servicio.llave;

  const encontrado = (o) => {
    setObjeto(o);
    setValores(valoresDesdeObjeto(entidad.campos, o));
  };

  const guardar = async () => {
    setAviso(null);
    try {
      const datos = validar(entidad.campos, valores, false);
      if (!window.confirm(`¿Guardar los cambios del ${entidad.nombre} con ID ${objeto[llave]}?`)) return;
      setGuardando(true);
      const actualizado = await entidad.servicio.actualizar(objeto[llave], datos);
      encontrado(actualizado);
      setAviso({ tipo: 'exito', texto: `El ${entidad.nombre} “${actualizado.nombre}” se actualizó correctamente.` });
    } catch (e) {
      setAviso(avisoDeError(e));
    } finally {
      setGuardando(false);
    }
  };

  return (
    <Ventana titulo={`Actualizar ${entidad.nombre}`} rol={entidad.rol} onCerrar={onCerrar}
      descripcion="Busque el registro, revise su información actual y modifique uno o varios atributos.">
      <Buscador servicio={entidad.servicio}
        onInicio={() => { setObjeto(null); setAviso(null); }}
        onEncontrado={encontrado}
        onError={(e) => setAviso(avisoDeError(e))} />
      <Aviso aviso={aviso} />
      <div className="dos-columnas">
        <Ficha campos={entidad.campos} objeto={objeto} titulo="Información actual" />
        {objeto && (
          <section className="ficha">
            <h2>Nuevos datos</h2>
            <Formulario campos={entidad.campos} valores={valores} onCambio={setValores}
              bloqueados={[llave]} buscarReferencias={entidad.proveedorReferencias} mostrarAyuda={false} />
          </section>
        )}
      </div>
      <div className="acciones">
        <button type="button" className="boton boton--primario" onClick={guardar} disabled={!objeto || guardando}>
          {guardando ? 'Guardando…' : 'Guardar cambios'}
        </button>
      </div>
    </Ventana>
  );
}
