import { formatear } from '../modelo/formato.js';

/** Grilla de resultados. Las columnas marcadas "delOtro" vienen de la otra colección. */
export default function Grilla({ columnas, filas }) {
  if (!filas.length) return <p className="vacio">No hay registros para mostrar con este filtro.</p>;
  return (
    <div className="grilla">
      <table>
        <thead>
          <tr>
            {columnas.map((c) => (
              <th key={c.clave} className={c.delOtro ? 'del-otro' : undefined} scope="col">{c.titulo}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {filas.map((f, i) => (
            <tr key={i}>
              {columnas.map((c) => {
                const numerico = c.tipo === 'entero' || c.tipo === 'decimal';
                const clase = [numerico && 'num', c.delOtro && 'del-otro'].filter(Boolean).join(' ');
                return (
                  <td key={c.clave} className={clase || undefined}>
                    {c.tipo === 'estado' && f[c.clave]
                      ? <span className={`estado estado--${f[c.clave].toLowerCase()}`}>{f[c.clave]}</span>
                      : formatear(c.tipo, f[c.clave])}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
