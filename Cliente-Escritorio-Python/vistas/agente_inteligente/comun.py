"""Configuracion compartida por las ventanas del agente inteligente."""
from modelo.campos import CAMPOS_AGENTE_INTELIGENTE
from servicios.notificador import AGENTE_INTELIGENTE
from servicios.servicio_agente_inteligente import ServicioAgenteInteligente


class ConfigAgenteInteligente:
    nombre_entidad = "agente inteligente"
    nombre_plural = "agentes inteligentes"
    campos = CAMPOS_AGENTE_INTELIGENTE
    servicio_cls = ServicioAgenteInteligente
    eventos_observados = [AGENTE_INTELIGENTE]
