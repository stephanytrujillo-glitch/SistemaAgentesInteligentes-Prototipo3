"""Cliente HTTP para el servidor GraphQL (patron Singleton)."""
import requests

from config import URL_GRAPHQL
from servicios.excepciones import ErrorConexion, ErrorServidor


class ClienteGraphQL:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.url = URL_GRAPHQL
            cls._instancia.sesion = requests.Session()
        return cls._instancia

    def ejecutar(self, consulta: str, variables: dict = None) -> dict:
        """Envia una operacion GraphQL usando VARIABLES (nunca concatenando valores en la consulta)."""
        try:
            respuesta = self.sesion.post(
                self.url,
                json={"query": consulta, "variables": variables or {}},
                timeout=10,
            )
        except requests.exceptions.ConnectionError:
            raise ErrorConexion(
                f"No se pudo conectar con el servidor en {self.url}.\n"
                "Verifique que el servidor Java y MongoDB estén en ejecución."
            )
        except requests.exceptions.Timeout:
            raise ErrorConexion("El servidor tardó demasiado en responder. Intente de nuevo.")

        try:
            cuerpo = respuesta.json()
        except ValueError:
            raise ErrorServidor(f"Respuesta inválida del servidor (HTTP {respuesta.status_code}).")

        if cuerpo.get("errors"):
            mensajes = [e.get("message", "Error desconocido") for e in cuerpo["errors"]]
            raise ErrorServidor("\n".join(mensajes))
        return cuerpo.get("data") or {}
