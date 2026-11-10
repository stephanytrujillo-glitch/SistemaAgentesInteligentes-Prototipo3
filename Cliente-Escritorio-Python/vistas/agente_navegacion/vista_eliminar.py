"""Ventana: Eliminar agente de navegación (un solo caso de uso)."""
from vistas.agente_navegacion.comun import ConfigAgenteNavegacion
from vistas.casos_base import VentanaEliminar


class VistaEliminarAgenteNavegacion(ConfigAgenteNavegacion, VentanaEliminar):
    pass
