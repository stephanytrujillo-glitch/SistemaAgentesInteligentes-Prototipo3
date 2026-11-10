"""Ventana: Adicionar agente inteligente (un solo caso de uso)."""
from vistas.agente_inteligente.comun import ConfigAgenteInteligente
from vistas.casos_base import VentanaAdicionar


class VistaAdicionarAgenteInteligente(ConfigAgenteInteligente, VentanaAdicionar):
    pass
