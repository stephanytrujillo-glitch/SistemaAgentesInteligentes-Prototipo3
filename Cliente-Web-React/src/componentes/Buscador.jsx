import { useState } from 'react';
import { ErrorValidacion } from '../modelo/validador.js';

/** Búsqueda previa de UN objeto por ID o por nombre. */
export default function Buscador({ servicio, onEncontrado, onError, onInicio }) {
  const [criterio, setCriterio] = useState('id');
  const [valor, setValor] = useState('');
  const [cargando, setCargando] = useState(false);

  const buscar = async (e) => {
    e.preventDefault();
    onInicio?.();
    const texto = valor.trim();
    try {
      if (!texto) throw new ErrorValidacion([`Escriba el ${criterio === 'id' ? 'ID' : 'nombre'} a buscar.`]);
      let objeto;
      if (criterio === 'id') {
        const id = Number(texto);
        if (!Number.isInteger(id) || id <= 0) throw new ErrorValidacion(['El ID debe ser un entero positivo.']);
        setCargando(true);
        objeto = await servicio.buscarPorId(id);
      } else {
        setCargando(true);
        objeto = await servicio.buscarPorNombre(texto);
      }
      onEncontrado(objeto);
    } catch (err) {
      onError(err);
    } finally {
      setCargando(false);
    }
  };

  return (
    <form className="buscador" onSubmit={buscar}>
      <label htmlFor="criterio">Buscar por</label>
      <select id="criterio" value={criterio} onChange={(e) => setCriterio(e.target.value)}>
        <option value="id">ID</option>
        <option value="nombre">Nombre</option>
      </select>
      <input aria-label={criterio === 'id' ? 'ID a buscar' : 'Nombre a buscar'} value={valor}
        onChange={(e) => setValor(e.target.value)} placeholder={criterio === 'id' ? 'Ej. 1' : 'Ej. Atlas'} />
      <button type="submit" className="boton boton--primario" disabled={cargando}>
        {cargando ? 'Buscando…' : 'Buscar'}
      </button>
    </form>
  );
}
