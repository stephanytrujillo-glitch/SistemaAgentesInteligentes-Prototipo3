import { CAMPOS_AGENTE_INTELIGENTE, CAMPOS_AGENTE_NAVEGACION, ESTADOS_OPERATIVOS } from '../modelo/campos.js';
import servicioAgenteInteligente from '../servicios/servicioAgenteInteligente.js';
import servicioAgenteNavegacion from '../servicios/servicioAgenteNavegacion.js';
import { AGENTE_INTELIGENTE, AGENTE_NAVEGACION } from '../servicios/notificador.js';

/** Qué clase gestiona cada grupo de vistas: campos, servicio, columnas de la grilla y filtros. */
export const ENTIDADES = {
  agente: {
    id: 'agente',
    rol: 'maestro',
    nombre: 'agente inteligente',
    plural: 'agentes inteligentes',
    campos: CAMPOS_AGENTE_INTELIGENTE,
    servicio: servicioAgenteInteligente,
    avisoEliminar: 'Sus agentes de navegación no se borran: quedarán sin agente asignado.',
    proveedorReferencias: null,
    eventosObservados: [AGENTE_INTELIGENTE],
    columnas: [
      { clave: 'idAgente', titulo: 'ID', tipo: 'entero' },
      { clave: 'nombre', titulo: 'Nombre', tipo: 'texto' },
      { clave: 'nivelAutonomia', titulo: 'Autonomía %', tipo: 'decimal' },
      { clave: 'estadoOperativo', titulo: 'Estado', tipo: 'estado' },
      { clave: 'nivelConfianza', titulo: 'Confianza %', tipo: 'decimal' },
      { clave: 'fechaRegistro', titulo: 'Registro', tipo: 'fecha' },
      { clave: 'aprendizajeContinuo', titulo: 'Aprendizaje', tipo: 'booleano' },
      { clave: 'descripcion', titulo: 'Descripción', tipo: 'texto' },
      { clave: 'cantidadNavegaciones', titulo: 'N.º navegaciones', tipo: 'entero', delOtro: true },
      { clave: 'precisionPromedio', titulo: 'Precisión GPS prom.', tipo: 'decimal', delOtro: true },
    ],
    filtros: [
      { clave: null, etiqueta: 'Todos' },
      { clave: 'estado', etiqueta: 'Estado operativo', tipo: 'opcion', opciones: ESTADOS_OPERATIVOS },
    ],
    listar: (filtro, valor, pagina, tamano) =>
      servicioAgenteInteligente.listar(filtro === 'estado' ? valor : null, pagina, tamano),
  },

  navegacion: {
    id: 'navegacion',
    rol: 'detalle',
    nombre: 'agente de navegación',
    plural: 'agentes de navegación',
    campos: CAMPOS_AGENTE_NAVEGACION,
    servicio: servicioAgenteNavegacion,
    avisoEliminar: '',
    // búsqueda en el servidor (máx. 20 coincidencias) en lugar de cargar todos los agentes
    proveedorReferencias: (texto) => servicioAgenteInteligente.opciones(texto),
    // la grilla muestra datos del agente inteligente, así que también observa sus cambios
    eventosObservados: [AGENTE_NAVEGACION, AGENTE_INTELIGENTE],
    columnas: [
      { clave: 'idNavegacion', titulo: 'ID', tipo: 'entero' },
      { clave: 'nombre', titulo: 'Nombre', tipo: 'texto' },
      { clave: 'origen', titulo: 'Origen', tipo: 'texto' },
      { clave: 'destino', titulo: 'Destino', tipo: 'texto' },
      { clave: 'precisionGPS', titulo: 'Precisión GPS %', tipo: 'decimal' },
      { clave: 'velocidadMaxima', titulo: 'Vel. máx. km/h', tipo: 'decimal' },
      { clave: 'fechaUltimaCalibracion', titulo: 'Última calibración', tipo: 'fecha' },
      { clave: 'rutaOptimizada', titulo: 'Ruta optimizada', tipo: 'booleano' },
      { clave: 'idAgenteInteligente', titulo: 'ID agente', tipo: 'referencia' },
      { clave: 'nombreAgente', titulo: 'Agente inteligente', tipo: 'texto', delOtro: true },
      { clave: 'estadoAgente', titulo: 'Estado del agente', tipo: 'estado', delOtro: true },
    ],
    filtros: [
      { clave: null, etiqueta: 'Todos' },
      { clave: 'destino', etiqueta: 'Destino', tipo: 'texto' },
      { clave: 'agente', etiqueta: 'Agente inteligente', tipo: 'referencia' },
    ],
    listar: (filtro, valor, pagina, tamano) => {
      if (filtro === 'destino') return servicioAgenteNavegacion.listarPorDestino(valor, pagina, tamano);
      if (filtro === 'agente') return servicioAgenteNavegacion.listarPorAgente(Number(valor), pagina, tamano);
      return servicioAgenteNavegacion.listarPorDestino('', pagina, tamano);
    },
  },
};

export const CASOS = [
  { id: 'adicionar', etiqueta: 'Adicionar' },
  { id: 'consultar', etiqueta: 'Consultar' },
  { id: 'listar', etiqueta: 'Listar' },
  { id: 'actualizar', etiqueta: 'Actualizar' },
  { id: 'eliminar', etiqueta: 'Eliminar' },
];
