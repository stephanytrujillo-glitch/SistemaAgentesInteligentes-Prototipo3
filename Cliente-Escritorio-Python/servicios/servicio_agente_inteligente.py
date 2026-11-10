"""Consumo de los servicios GraphQL del agente inteligente (maestro)."""
from modelo.agente_inteligente import AgenteInteligente
from servicios.cliente_graphql import ClienteGraphQL
from servicios.notificador import AGENTE_INTELIGENTE, AGENTE_NAVEGACION, Notificador

CAMPOS = "idAgente nombre nivelAutonomia estadoOperativo nivelConfianza fechaRegistro aprendizajeContinuo descripcion"
CAMPOS_RESUMEN = CAMPOS + " cantidadNavegaciones precisionPromedio"

CREAR = """
mutation Crear($input: AgenteInteligenteInput!) {
  crearAgenteInteligente(input: $input) { %s }
}""" % CAMPOS

ACTUALIZAR = """
mutation Actualizar($id: Int!, $input: ActualizarAgenteInteligenteInput!) {
  actualizarAgenteInteligente(idAgente: $id, input: $input) { %s }
}""" % CAMPOS

ELIMINAR = """
mutation Eliminar($id: Int!) {
  eliminarAgenteInteligente(idAgente: $id)
}"""

POR_ID = """
query PorId($id: Int!) {
  agenteInteligentePorId(idAgente: $id) { %s }
}""" % CAMPOS

POR_NOMBRE = """
query PorNombre($nombre: String!) {
  agenteInteligentePorNombre(nombre: $nombre) { %s }
}""" % CAMPOS

# Listado PAGINADO: el servidor solo devuelve una pagina (tamano registros) y el total
LISTAR_RESUMEN = """
query Listar($estado: EstadoOperativo, $pagina: Int, $tamano: Int) {
  agentesInteligentesResumen(estado: $estado, pagina: $pagina, tamano: $tamano) {
    elementos { %s }
    total pagina tamano totalPaginas
  }
}""" % CAMPOS_RESUMEN

# Busqueda de pocas opciones (por nombre o ID) en lugar de traer todos los agentes
OPCIONES = """
query Opciones($texto: String, $limite: Int) {
  agentesInteligentesOpciones(texto: $texto, limite: $limite) { idAgente nombre }
}"""


class ServicioAgenteInteligente:
    LLAVE = "idAgente"

    def __init__(self):
        self._cliente = ClienteGraphQL()

    def crear(self, datos: dict) -> AgenteInteligente:
        r = self._cliente.ejecutar(CREAR, {"input": datos})
        Notificador().notificar(AGENTE_INTELIGENTE)
        return AgenteInteligente.desde_dict(r["crearAgenteInteligente"])

    def actualizar(self, id_agente: int, datos: dict) -> AgenteInteligente:
        r = self._cliente.ejecutar(ACTUALIZAR, {"id": id_agente, "input": datos})
        Notificador().notificar(AGENTE_INTELIGENTE)
        return AgenteInteligente.desde_dict(r["actualizarAgenteInteligente"])

    def eliminar(self, id_agente: int) -> str:
        mensaje = self._cliente.ejecutar(ELIMINAR, {"id": id_agente})["eliminarAgenteInteligente"]
        Notificador().notificar(AGENTE_INTELIGENTE)
        Notificador().notificar(AGENTE_NAVEGACION)  # sus navegaciones quedan sin agente
        return mensaje

    def buscar_por_id(self, id_agente: int) -> AgenteInteligente:
        r = self._cliente.ejecutar(POR_ID, {"id": id_agente})
        return AgenteInteligente.desde_dict(r["agenteInteligentePorId"])

    def buscar_por_nombre(self, nombre: str) -> AgenteInteligente:
        r = self._cliente.ejecutar(POR_NOMBRE, {"nombre": nombre})
        return AgenteInteligente.desde_dict(r["agenteInteligentePorNombre"])

    def listar(self, estado: str = None, pagina: int = 0, tamano: int = 25) -> dict:
        """Una pagina de agentes (todos si estado=None), con 2 datos del detalle.

        Devuelve {"elementos": [...], "total", "pagina", "tamano", "totalPaginas"}.
        """
        variables = {"estado": estado, "pagina": pagina, "tamano": tamano}
        return self._cliente.ejecutar(LISTAR_RESUMEN, variables)["agentesInteligentesResumen"]

    def opciones(self, texto: str = "", limite: int = 20) -> list:
        """Hasta 'limite' pares (id, nombre) cuyo nombre contiene el texto o cuyo ID es el texto."""
        filas = self._cliente.ejecutar(OPCIONES, {"texto": texto, "limite": limite})["agentesInteligentesOpciones"]
        return [(f["idAgente"], f["nombre"]) for f in filas]
