"""Excepciones del cliente al comunicarse con el servidor."""


class ErrorConexion(Exception):
    """No fue posible comunicarse con el servidor GraphQL."""


class ErrorServidor(Exception):
    """El servidor respondio con errores GraphQL (validacion, no encontrado, etc.)."""
