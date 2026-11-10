import { URL_GRAPHQL } from '../config/app.js';

/** Cliente GraphQL (patrón Singleton). Los parámetros siempre viajan como VARIABLES. */
class ClienteGraphQL {
  static #instancia = null;

  static obtener() {
    if (!ClienteGraphQL.#instancia) ClienteGraphQL.#instancia = new ClienteGraphQL(URL_GRAPHQL);
    return ClienteGraphQL.#instancia;
  }

  constructor(url) {
    this.url = url;
  }

  async ejecutar(consulta, variables = {}) {
    let respuesta;
    try {
      respuesta = await fetch(this.url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: consulta, variables }),
      });
    } catch {
      throw new Error(`No se pudo conectar con el servidor en ${this.url}. Verifique que el servidor Java y MongoDB estén en ejecución.`);
    }
    let cuerpo;
    try {
      cuerpo = await respuesta.json();
    } catch {
      throw new Error(`Respuesta inválida del servidor (HTTP ${respuesta.status}).`);
    }
    if (cuerpo.errors?.length) {
      throw new Error(cuerpo.errors.map((e) => e.message).join('\n'));
    }
    return cuerpo.data ?? {};
  }
}

export default ClienteGraphQL;
