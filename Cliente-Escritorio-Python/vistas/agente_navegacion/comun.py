"""Configuracion compartida por las ventanas del agente de navegacion."""
from modelo.campos import CAMPOS_AGENTE_NAVEGACION
from servicios.notificador import AGENTE_INTELIGENTE, AGENTE_NAVEGACION
from servicios.servicio_agente_inteligente import ServicioAgenteInteligente
from servicios.servicio_agente_navegacion import ServicioAgenteNavegacion


class ConfigAgenteNavegacion:
    nombre_entidad = "agente de navegación"
    nombre_plural = "agentes de navegación"
    campos = CAMPOS_AGENTE_NAVEGACION
    servicio_cls = ServicioAgenteNavegacion
    # la grilla muestra datos del agente inteligente, asi que tambien observa sus cambios
    eventos_observados = [AGENTE_NAVEGACION, AGENTE_INTELIGENTE]

    def proveedor_referencias(self):
        return ServicioAgenteInteligente().opciones
