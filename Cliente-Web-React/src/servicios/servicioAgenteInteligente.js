import ClienteGraphQL from './clienteGraphQL.js';
import AgenteInteligente from '../modelo/AgenteInteligente.js';
import Notificador, { AGENTE_INTELIGENTE, AGENTE_NAVEGACION } from './notificador.js';

const CAMPOS = 'idAgente nombre nivelAutonomia estadoOperativo nivelConfianza fechaRegistro aprendizajeContinuo descripcion';
const CAMPOS_RESUMEN = `${CAMPOS} cantidadNavegaciones precisionPromedio`;

const CREAR = `mutation Crear($input: AgenteInteligenteInput!) {
  crearAgenteInteligente(input: $input) { ${CAMPOS} }
}`;
const ACTUALIZAR = `mutation Actualizar($id: Int!, $input: ActualizarAgenteInteligenteInput!) {
  actualizarAgenteInteligente(idAgente: $id, input: $input) { ${CAMPOS} }
}`;
const ELIMINAR = `mutation Eliminar($id: Int!) { eliminarAgenteInteligente(idAgente: $id) }`;
const POR_ID = `query PorId($id: Int!) { agenteInteligentePorId(idAgente: $id) { ${CAMPOS} } }`;
const POR_NOMBRE = `query PorNombre($nombre: String!) { agenteInteligentePorNombre(nombre: $nombre) { ${CAMPOS} } }`;
// Listado PAGINADO: el servidor solo devuelve una página y el total
const LISTAR = `query Listar($estado: EstadoOperativo, $pagina: Int, $tamano: Int) {
  agentesInteligentesResumen(estado: $estado, pagina: $pagina, tamano: $tamano) {
    elementos { ${CAMPOS_RESUMEN} }
    total pagina tamano totalPaginas
  }
}`;
// Pocas opciones (búsqueda por nombre o ID) en lugar de traer todos los agentes
const OPCIONES = `query Opciones($texto: String, $limite: Int) {
  agentesInteligentesOpciones(texto: $texto, limite: $limite) { idAgente nombre }
}`;

const cliente = () => ClienteGraphQL.obtener();

const servicioAgenteInteligente = {
  llave: 'idAgente',

  async crear(datos) {
    const r = await cliente().ejecutar(CREAR, { input: datos });
    Notificador.obtener().notificar(AGENTE_INTELIGENTE);
    return AgenteInteligente.desdeDatos(r.crearAgenteInteligente);
  },
  async actualizar(id, datos) {
    const r = await cliente().ejecutar(ACTUALIZAR, { id, input: datos });
    Notificador.obtener().notificar(AGENTE_INTELIGENTE);
    return AgenteInteligente.desdeDatos(r.actualizarAgenteInteligente);
  },
  async eliminar(id) {
    const r = await cliente().ejecutar(ELIMINAR, { id });
    Notificador.obtener().notificar(AGENTE_INTELIGENTE);
    Notificador.obtener().notificar(AGENTE_NAVEGACION); // sus navegaciones quedan sin agente
    return r.eliminarAgenteInteligente;
  },
  async buscarPorId(id) {
    const r = await cliente().ejecutar(POR_ID, { id });
    return AgenteInteligente.desdeDatos(r.agenteInteligentePorId);
  },
  async buscarPorNombre(nombre) {
    const r = await cliente().ejecutar(POR_NOMBRE, { nombre });
    return AgenteInteligente.desdeDatos(r.agenteInteligentePorNombre);
  },
  /** Una página (todos si estado es null) con 2 datos del detalle: { elementos, total, pagina, tamano, totalPaginas }. */
  async listar(estado = null, pagina = 0, tamano = 25) {
    const r = await cliente().ejecutar(LISTAR, { estado, pagina, tamano });
    return r.agentesInteligentesResumen;
  },
  /** Hasta `limite` agentes [{ id, nombre }] cuyo nombre contiene el texto o cuyo ID es el texto. */
  async opciones(texto = '', limite = 20) {
    const r = await cliente().ejecutar(OPCIONES, { texto, limite });
    return r.agentesInteligentesOpciones.map((a) => ({ id: a.idAgente, nombre: a.nombre }));
  },
};

export default servicioAgenteInteligente;
