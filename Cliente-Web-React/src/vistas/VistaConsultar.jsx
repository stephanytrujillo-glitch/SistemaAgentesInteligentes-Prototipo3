import { useState } from 'react';
import Ventana from '../componentes/Ventana.jsx';
import Buscador from '../componentes/Buscador.jsx';
import Ficha from '../componentes/Ficha.jsx';
import Aviso, { avisoDeError } from '../componentes/Aviso.jsx';

/** Caso de uso: Consultar UN SOLO objeto a partir de un parámetro (ID o nombre). */
export default function VistaConsultar({ entidad, onCerrar }) {
  const [objeto, setObjeto] = useState(null);
  const [aviso, setAviso] = useState(null);

  return (
    <Ventana titulo={`Consultar ${entidad.nombre}`} rol={entidad.rol} onCerrar={onCerrar}
      descripcion="Consulte un registro escribiendo su ID o su nombre.">
      <Buscador servicio={entidad.servicio}
        onInicio={() => { setObjeto(null); setAviso(null); }}
        onEncontrado={setObjeto}
        onError={(e) => setAviso(avisoDeError(e))} />
      <Aviso aviso={aviso} />
      <Ficha campos={entidad.campos} objeto={objeto} titulo={`Datos del ${entidad.nombre}`} />
    </Ventana>
  );
}
