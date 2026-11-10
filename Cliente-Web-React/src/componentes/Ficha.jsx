import { formatear } from '../modelo/formato.js';

/** Muestra TODA la información de un objeto en modo solo lectura. */
export default function Ficha({ campos, objeto, titulo = 'Información del registro' }) {
  return (
    <section className="ficha">
      <h2>{titulo}</h2>
      {objeto ? (
        <dl>
          {campos.map((c) => (
            <div key={c.clave}>
              <dt>{c.etiqueta}</dt>
              <dd>{formatear(c.tipo, objeto[c.clave])}</dd>
            </div>
          ))}
        </dl>
      ) : (
        <p className="vacio">Busque un registro por ID o por nombre para ver su información.</p>
      )}
    </section>
  );
}
