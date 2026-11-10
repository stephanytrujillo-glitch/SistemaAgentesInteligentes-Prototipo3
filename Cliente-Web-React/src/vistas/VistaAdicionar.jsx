import { useState } from 'react';
import Ventana from '../componentes/Ventana.jsx';
import Formulario from '../componentes/Formulario.jsx';
import Aviso, { avisoDeError } from '../componentes/Aviso.jsx';
import { validar, valoresVacios } from '../modelo/validador.js';

/** Caso de uso: Adicionar (un nuevo objeto de la clase). */
export default function VistaAdicionar({ entidad, onCerrar }) {
  const [valores, setValores] = useState(() => valoresVacios(entidad.campos));
  const [aviso, setAviso] = useState(null);
  const [guardando, setGuardando] = useState(false);

  const guardar = async () => {
    setAviso(null);
    try {
      const datos = validar(entidad.campos, valores);
      setGuardando(true);
      const objeto = await entidad.servicio.crear(datos);
      setAviso({ tipo: 'exito', texto: `El ${entidad.nombre} “${objeto.nombre}” se guardó correctamente.` });
      setValores(valoresVacios(entidad.campos));
    } catch (e) {
      setAviso(avisoDeError(e));
    } finally {
      setGuardando(false);
    }
  };

  return (
    <Ventana titulo={`Adicionar ${entidad.nombre}`} rol={entidad.rol} onCerrar={onCerrar}
      descripcion="Complete los datos y guarde el nuevo registro.">
      <Formulario campos={entidad.campos} valores={valores} onCambio={setValores} buscarReferencias={entidad.proveedorReferencias} />
      <Aviso aviso={aviso} />
      <div className="acciones">
        <button type="button" className="boton" onClick={() => { setValores(valoresVacios(entidad.campos)); setAviso(null); }}>
          Limpiar
        </button>
        <button type="button" className="boton boton--primario" onClick={guardar} disabled={guardando}>
          {guardando ? 'Guardando…' : 'Guardar'}
        </button>
      </div>
    </Ventana>
  );
}
