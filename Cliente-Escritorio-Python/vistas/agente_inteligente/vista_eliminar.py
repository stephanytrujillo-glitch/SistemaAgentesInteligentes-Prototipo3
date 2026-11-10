"""Ventana: Eliminar agente inteligente (un solo caso de uso)."""
from vistas.agente_inteligente.comun import ConfigAgenteInteligente
from vistas.casos_base import VentanaEliminar


class VistaEliminarAgenteInteligente(ConfigAgenteInteligente, VentanaEliminar):
    aviso_eliminar = "Sus agentes de navegación NO se borran: quedarán sin agente asignado."
