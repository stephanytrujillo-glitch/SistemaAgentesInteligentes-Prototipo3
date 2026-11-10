/** Mensajes de resultado, advertencia o error. */
export default function Aviso({ aviso }) {
  if (!aviso) return null;
  return (
    <div className={`aviso aviso--${aviso.tipo}`} role={aviso.tipo === 'exito' ? 'status' : 'alert'}>
      {aviso.titulo && <strong>{aviso.titulo}</strong>}
      {aviso.lista ? (
        <ul>{aviso.lista.map((t) => <li key={t}>{t}</li>)}</ul>
      ) : (
        <p>{aviso.texto}</p>
      )}
    </div>
  );
}

export function avisoDeError(error) {
  if (error?.errores) return { tipo: 'advertencia', titulo: 'Revise los datos', lista: error.errores };
  const lineas = String(error?.message ?? error).split('\n');
  return lineas.length > 1
    ? { tipo: 'error', titulo: 'Operación no realizada', lista: lineas }
    : { tipo: 'error', titulo: 'Operación no realizada', texto: lineas[0] };
}
