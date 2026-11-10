import { useEffect, useRef } from 'react';
import { CURSO, INTEGRANTES, NOMBRE_APP, TECNOLOGIA, VERSION } from '../config/app.js';

/** Ayuda > Acerca de... */
export default function AcercaDe({ onCerrar }) {
  const boton = useRef(null);
  useEffect(() => {
    boton.current?.focus();
    const escape = (e) => { if (e.key === 'Escape') onCerrar(); };
    document.addEventListener('keydown', escape);
    return () => document.removeEventListener('keydown', escape);
  }, [onCerrar]);

  return (
    <div className="dialogo-fondo" onMouseDown={(e) => { if (e.target === e.currentTarget) onCerrar(); }}>
      <div className="dialogo" role="dialog" aria-modal="true" aria-labelledby="titulo-acerca">
        <h2 id="titulo-acerca">{NOMBRE_APP}</h2>
        <p className="version">Versión {VERSION}</p>
        <p className="nota">{TECNOLOGIA}<br />{CURSO}</p>
        <h3>Integrantes del equipo</h3>
        <ul>{INTEGRANTES.map((n) => <li key={n}>{n}</li>)}</ul>
        <button ref={boton} type="button" className="boton boton--primario" onClick={onCerrar}>Cerrar</button>
      </div>
    </div>
  );
}
