import ClienteGraphQL from './clienteGraphQL.js';
import AgenteNavegacion from '../modelo/AgenteNavegacion.js';
import Notificador, { AGENTE_NAVEGACION } from './notificador.js';

const CAMPOS = 'idNavegacion nombre origen destino precisionGPS velocidadMaxima fechaUltimaCalibracion rutaOptimizada idAgenteInteligente';
const CAMPOS_LISTA = `${CAMPOS} nombreAgente estadoAgente`;

const CREAR = `mutation Crear($input: AgenteNavegacionInput!) {
  crearAgenteNavegacion(input: $input) { ${CAMPOS} }
}`;
const ACTUALIZAR = `mutation Actualizar($id: Int!, $input: ActualizarAgenteNavegacionInput!) {
  actualizarAgenteNavegacion(idNavegacion: $id, input: $input) { ${CAMPOS} }
}`;
const ELIMINAR = `mutation Eliminar($id: Int!) { eliminarAgenteNavegacion(idNavegacion: $id) }`;
const POR_ID = `query PorId($id: Int!) { agenteNavegacionPorId(idNavegacion: $id) { ${CAMPOS} } }`;
const POR_NOMBRE = `query PorNombre($nombre: String!) { agenteNavegacionPorNombre(nombre: $nombre) { ${CAMPOS} } }`;
// Listados PAGINADOS: el servidor solo devuelve una página y el total
const PAGINA = `total pagina tamano totalPaginas`;
const LISTAR_POR_DESTINO = `query ListarPorDestino($destino: String, $pagina: Int, $tamano: Int) {
  navegacionesConAgente(destino: $destino, pagina: $pagina, tamano: $tamano) {
    elementos { ${CAMPOS_LISTA} } ${PAGINA}
  }
}`;
const LISTAR_POR_AGENTE = `query ListarPorAgente($idAgente: Int!, $pagina: Int, $tamano: Int) {
  navegacionesPorAgente(idAgente: $idAgente, pagina: $pagina, tamano: $tamano) {
    elementos { ${CAMPOS_LISTA} } ${PAGINA}
  }
}`;

const cliente = () => ClienteGraphQL.obtener();

const servicioAgenteNavegacion = {
  llave: 'idNavegacion',

  async crear(datos) {
    const r = await cliente().ejecutar(CREAR, { input: datos });
    Notificador.obtener().notificar(AGENTE_NAVEGACION);
    return AgenteNavegacion.desdeDatos(r.crearAgenteNavegacion);
  },
  async actualizar(id, datos) {
    const r = await cliente().ejecutar(ACTUALIZAR, { id, input: datos });
    Notificador.obtener().notificar(AGENTE_NAVEGACION);
    return AgenteNavegacion.desdeDatos(r.actualizarAgenteNavegacion);
  },
  async eliminar(id) {
    const r = await cliente().ejecutar(ELIMINAR, { id });
    Notificador.obtener().notificar(AGENTE_NAVEGACION);
    return r.eliminarAgenteNavegacion;
  },
  async buscarPorId(id) {
    const r = await cliente().ejecutar(POR_ID, { id });
    return AgenteNavegacion.desdeDatos(r.agenteNavegacionPorId);
  },
  async buscarPorNombre(nombre) {
    const r = await cliente().ejecutar(POR_NOMBRE, { nombre });
    return AgenteNavegacion.desdeDatos(r.agenteNavegacionPorNombre);
  },
  /** Una página (todos si destino vacío); incluye nombre y estado del agente inteligente. */
  async listarPorDestino(destino = '', pagina = 0, tamano = 25) {
    const r = await cliente().ejecutar(LISTAR_POR_DESTINO, { destino, pagina, tamano });
    return r.navegacionesConAgente;
  },
  async listarPorAgente(idAgente, pagina = 0, tamano = 25) {
    const r = await cliente().ejecutar(LISTAR_POR_AGENTE, { idAgente, pagina, tamano });
    return r.navegacionesPorAgente;
  },
};

export default servicioAgenteNavegacion;
