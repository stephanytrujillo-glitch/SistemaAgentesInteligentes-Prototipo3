"""Consumo de los servicios GraphQL del agente de navegacion (detalle)."""
from modelo.agente_navegacion import AgenteNavegacion
from servicios.cliente_graphql import ClienteGraphQL
from servicios.notificador import AGENTE_NAVEGACION, Notificador

CAMPOS = ("idNavegacion nombre origen destino precisionGPS velocidadMaxima "
          "fechaUltimaCalibracion rutaOptimizada idAgenteInteligente")
CAMPOS_LISTA = CAMPOS + " nombreAgente estadoAgente"

CREAR = """
mutation Crear($input: AgenteNavegacionInput!) {
  crearAgenteNavegacion(input: $input) { %s }
}""" % CAMPOS

ACTUALIZAR = """
mutation Actualizar($id: Int!, $input: ActualizarAgenteNavegacionInput!) {
  actualizarAgenteNavegacion(idNavegacion: $id, input: $input) { %s }
}""" % CAMPOS

ELIMINAR = """
mutation Eliminar($id: Int!) {
  eliminarAgenteNavegacion(idNavegacion: $id)
}"""

POR_ID = """
query PorId($id: Int!) {
  agenteNavegacionPorId(idNavegacion: $id) { %s }
}""" % CAMPOS

POR_NOMBRE = """
query PorNombre($nombre: String!) {
  agenteNavegacionPorNombre(nombre: $nombre) { %s }
}""" % CAMPOS

# Listados PAGINADOS: el servidor solo devuelve una pagina y el total
LISTAR_POR_DESTINO = """
query ListarPorDestino($destino: String, $pagina: Int, $tamano: Int) {
  navegacionesConAgente(destino: $destino, pagina: $pagina, tamano: $tamano) {
    elementos { %s }
    total pagina tamano totalPaginas
  }
}""" % CAMPOS_LISTA

LISTAR_POR_AGENTE = """
query ListarPorAgente($idAgente: Int!, $pagina: Int, $tamano: Int) {
  navegacionesPorAgente(idAgente: $idAgente, pagina: $pagina, tamano: $tamano) {
    elementos { %s }
    total pagina tamano totalPaginas
  }
}""" % CAMPOS_LISTA


class ServicioAgenteNavegacion:
    LLAVE = "idNavegacion"

    def __init__(self):
        self._cliente = ClienteGraphQL()

    def crear(self, datos: dict) -> AgenteNavegacion:
        r = self._cliente.ejecutar(CREAR, {"input": datos})
        Notificador().notificar(AGENTE_NAVEGACION)
        return AgenteNavegacion.desde_dict(r["crearAgenteNavegacion"])

    def actualizar(self, id_navegacion: int, datos: dict) -> AgenteNavegacion:
        r = self._cliente.ejecutar(ACTUALIZAR, {"id": id_navegacion, "input": datos})
        Notificador().notificar(AGENTE_NAVEGACION)
        return AgenteNavegacion.desde_dict(r["actualizarAgenteNavegacion"])

    def eliminar(self, id_navegacion: int) -> str:
        mensaje = self._cliente.ejecutar(ELIMINAR, {"id": id_navegacion})["eliminarAgenteNavegacion"]
        Notificador().notificar(AGENTE_NAVEGACION)
        return mensaje

    def buscar_por_id(self, id_navegacion: int) -> AgenteNavegacion:
        r = self._cliente.ejecutar(POR_ID, {"id": id_navegacion})
        return AgenteNavegacion.desde_dict(r["agenteNavegacionPorId"])

    def buscar_por_nombre(self, nombre: str) -> AgenteNavegacion:
        r = self._cliente.ejecutar(POR_NOMBRE, {"nombre": nombre})
        return AgenteNavegacion.desde_dict(r["agenteNavegacionPorNombre"])

    def listar_por_destino(self, destino: str = "", pagina: int = 0, tamano: int = 25) -> dict:
        """Una pagina (todos si destino vacio); incluye nombre y estado del agente inteligente."""
        variables = {"destino": destino, "pagina": pagina, "tamano": tamano}
        return self._cliente.ejecutar(LISTAR_POR_DESTINO, variables)["navegacionesConAgente"]

    def listar_por_agente(self, id_agente: int, pagina: int = 0, tamano: int = 25) -> dict:
        variables = {"idAgente": id_agente, "pagina": pagina, "tamano": tamano}
        return self._cliente.ejecutar(LISTAR_POR_AGENTE, variables)["navegacionesPorAgente"]
