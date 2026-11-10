"""Ventana: Consultar agente de navegación (un solo caso de uso)."""
from vistas.agente_navegacion.comun import ConfigAgenteNavegacion
from vistas.casos_base import VentanaConsultar


class VistaConsultarAgenteNavegacion(ConfigAgenteNavegacion, VentanaConsultar):
    pass
