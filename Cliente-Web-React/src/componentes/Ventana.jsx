/** Marco de "ventana": cada vista implementa un solo caso de uso. */
export default function Ventana({ titulo, descripcion, rol, onCerrar, children }) {
  return (
    <section className={`ventana ventana--${rol ?? 'neutra'}`} aria-labelledby="titulo-ventana">
      <header className="ventana__barra">
        <div>
          <h1 id="titulo-ventana">{titulo}</h1>
          {descripcion && <p>{descripcion}</p>}
        </div>
        {onCerrar && (
          <button type="button" className="ventana__cerrar" onClick={onCerrar} aria-label="Cerrar ventana">×</button>
        )}
      </header>
      <div className="ventana__cuerpo">{children}</div>
    </section>
  );
}
