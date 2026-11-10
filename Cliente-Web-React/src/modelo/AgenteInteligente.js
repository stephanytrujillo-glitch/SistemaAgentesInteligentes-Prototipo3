/** Clase estructural del maestro. */
export default class AgenteInteligente {
  constructor({ idAgente, nombre, nivelAutonomia, estadoOperativo, nivelConfianza = null,
    fechaRegistro, aprendizajeContinuo, descripcion = null }) {
    this.idAgente = idAgente;
    this.nombre = nombre;
    this.nivelAutonomia = nivelAutonomia;
    this.estadoOperativo = estadoOperativo;
    this.nivelConfianza = nivelConfianza;
    this.fechaRegistro = fechaRegistro;
    this.aprendizajeContinuo = aprendizajeContinuo;
    this.descripcion = descripcion;
  }

  static desdeDatos(datos) {
    return new AgenteInteligente(datos);
  }
}
