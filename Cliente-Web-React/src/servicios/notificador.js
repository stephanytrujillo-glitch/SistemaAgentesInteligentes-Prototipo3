/**
 * Patrón Observer: los servicios avisan cuando cambian los datos de una clase y
 * las vistas suscritas (grilla de Listar, listas de agentes en formularios) se actualizan solas.
 */
export const AGENTE_INTELIGENTE = 'agente_inteligente';
export const AGENTE_NAVEGACION = 'agente_navegacion';

class Notificador {
  static #instancia = null;
  #observadores = new Map();

  static obtener() {
    if (!Notificador.#instancia) Notificador.#instancia = new Notificador();
    return Notificador.#instancia;
  }

  /** Suscribe un observador y devuelve la función para cancelar la suscripción. */
  suscribir(evento, observador) {
    if (!this.#observadores.has(evento)) this.#observadores.set(evento, new Set());
    this.#observadores.get(evento).add(observador);
    return () => this.#observadores.get(evento)?.delete(observador);
  }

  notificar(evento) {
    for (const observador of [...(this.#observadores.get(evento) ?? [])]) {
      try { observador(evento); } catch { /* un observador con error no detiene a los demás */ }
    }
  }
}

export default Notificador;
