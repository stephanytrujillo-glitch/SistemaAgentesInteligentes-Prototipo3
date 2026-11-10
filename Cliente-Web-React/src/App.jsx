import { useState } from 'react';
import MenuPrincipal from './componentes/MenuPrincipal.jsx';
import AcercaDe from './componentes/AcercaDe.jsx';
import Inicio from './vistas/Inicio.jsx';
import VistaAdicionar from './vistas/VistaAdicionar.jsx';
import VistaConsultar from './vistas/VistaConsultar.jsx';
import VistaListar from './vistas/VistaListar.jsx';
import VistaActualizar from './vistas/VistaActualizar.jsx';
import VistaEliminar from './vistas/VistaEliminar.jsx';
import { ENTIDADES } from './config/entidades.js';

const VISTAS = {
  adicionar: VistaAdicionar,
  consultar: VistaConsultar,
  listar: VistaListar,
  actualizar: VistaActualizar,
  eliminar: VistaEliminar,
};

export default function App() {
  const [actual, setActual] = useState({ caso: 'inicio', entidad: null });
  const [acercaDe, setAcercaDe] = useState(false);

  const navegar = (caso, entidad) => setActual({ caso, entidad });
  const inicio = () => setActual({ caso: 'inicio', entidad: null });
  const Vista = VISTAS[actual.caso];

  return (
    <>
      <MenuPrincipal onNavegar={navegar} onAcercaDe={() => setAcercaDe(true)} onInicio={inicio} />
      <main className="escritorio">
        {Vista
          ? <Vista key={`${actual.caso}-${actual.entidad}`} entidad={ENTIDADES[actual.entidad]} onCerrar={inicio} />
          : <Inicio onNavegar={navegar} />}
      </main>
      {acercaDe && <AcercaDe onCerrar={() => setAcercaDe(false)} />}
    </>
  );
}
