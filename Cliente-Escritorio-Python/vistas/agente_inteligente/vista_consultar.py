"""Ventana: Consultar agente inteligente (un solo caso de uso)."""
from vistas.agente_inteligente.comun import ConfigAgenteInteligente
from vistas.casos_base import VentanaConsultar


class VistaConsultarAgenteInteligente(ConfigAgenteInteligente, VentanaConsultar):
    pass
