/** Clase estructural del detalle. */
export default class AgenteNavegacion {
  constructor({ idNavegacion, nombre, origen, destino, precisionGPS, velocidadMaxima = null,
    fechaUltimaCalibracion, rutaOptimizada, idAgenteInteligente = null }) {
    this.idNavegacion = idNavegacion;
    this.nombre = nombre;
    this.origen = origen;
    this.destino = destino;
    this.precisionGPS = precisionGPS;
    this.velocidadMaxima = velocidadMaxima;
    this.fechaUltimaCalibracion = fechaUltimaCalibracion;
    this.rutaOptimizada = rutaOptimizada;
    this.idAgenteInteligente = idAgenteInteligente;
  }

  static desdeDatos(datos) {
    return new AgenteNavegacion(datos);
  }
}
