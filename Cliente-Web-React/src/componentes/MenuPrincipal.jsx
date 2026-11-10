import { useEffect, useRef, useState } from 'react';
import { CASOS, ENTIDADES } from '../config/entidades.js';

/** Menú principal: un menú por clase y el menú Ayuda con "Acerca de...". */
export default function MenuPrincipal({ onNavegar, onAcercaDe, onInicio }) {
  const [abierto, setAbierto] = useState(null);
  const barra = useRef(null);

  useEffect(() => {
    const cerrar = (e) => { if (barra.current && !barra.current.contains(e.target)) setAbierto(null); };
    const escape = (e) => { if (e.key === 'Escape') setAbierto(null); };
    document.addEventListener('mousedown', cerrar);
    document.addEventListener('keydown', escape);
    return () => {
      document.removeEventListener('mousedown', cerrar);
      document.removeEventListener('keydown', escape);
    };
  }, []);

  const menus = [
    ...Object.values(ENTIDADES).map((e) => ({
      id: e.id,
      titulo: e.plural.charAt(0).toUpperCase() + e.plural.slice(1),
      items: CASOS.map((c) => ({ etiqueta: `${c.etiqueta}...`, accion: () => onNavegar(c.id, e.id) })),
    })),
    { id: 'ayuda', titulo: 'Ayuda', items: [{ etiqueta: 'Acerca de...', accion: onAcercaDe }] },
  ];

  return (
    <nav className="menu" ref={barra} aria-label="Menú principal">
      <button type="button" className="menu__marca" onClick={() => { setAbierto(null); onInicio(); }}>
        Agentes Inteligentes
      </button>
      {menus.map((m) => (
        <div key={m.id} className="menu__grupo">
          <button
            type="button"
            className="menu__boton"
            aria-haspopup="true"
            aria-expanded={abierto === m.id}
            onClick={() => setAbierto(abierto === m.id ? null : m.id)}
          >
            {m.titulo}
          </button>
          {abierto === m.id && (
            <ul className="menu__lista" role="menu">
              {m.items.map((it) => (
                <li key={it.etiqueta} role="none">
                  <button type="button" role="menuitem" onClick={() => { setAbierto(null); it.accion(); }}>
                    {it.etiqueta}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </nav>
  );
}
