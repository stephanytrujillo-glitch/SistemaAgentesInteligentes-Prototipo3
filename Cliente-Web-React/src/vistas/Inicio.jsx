import { useState } from 'react';
import Ventana from '../componentes/Ventana.jsx';
import ClienteGraphQL from '../servicios/clienteGraphQL.js';
import { CASOS, ENTIDADES } from '../config/entidades.js';
import { TECNOLOGIA, URL_GRAPHQL } from '../config/app.js';

/** Ventana principal: accesos a cada caso de uso y estado del servidor. */
export default function Inicio({ onNavegar }) {
  const [estado, setEstado] = useState('Sin verificar');

  const probar = async () => {
    setEstado('Verificando…');
    try {
      await ClienteGraphQL.obtener().ejecutar('query { __typename }');
      setEstado('Conectado');
    } catch (e) {
      setEstado(e.message);
    }
  };

  return (
    <Ventana titulo="Sistema de Agentes Inteligentes" descripcion={TECNOLOGIA}>
      <p className="intro">
        Gestione los agentes inteligentes (maestro) y sus agentes de navegación (detalle).
        Use el menú superior o los accesos de abajo; cada opción abre una ventana dedicada a un solo caso de uso.
      </p>
      <div className="accesos">
        {Object.values(ENTIDADES).map((e) => (
          <section key={e.id} className={`acceso acceso--${e.rol}`}>
            <h2>{e.plural.charAt(0).toUpperCase() + e.plural.slice(1)}</h2>
            <p className="nota">Colección {e.rol}</p>
            <div className="acceso__botones">
              {CASOS.map((c) => (
                <button key={c.id} type="button" className="boton" onClick={() => onNavegar(c.id, e.id)}>
                  {c.etiqueta}
                </button>
              ))}
            </div>
          </section>
        ))}
      </div>
      <div className="servidor">
        <span>Servidor GraphQL: <code>{URL_GRAPHQL}</code></span>
        <span className="nota">{estado}</span>
        <button type="button" className="boton" onClick={probar}>Probar conexión</button>
      </div>
    </Ventana>
  );
}
