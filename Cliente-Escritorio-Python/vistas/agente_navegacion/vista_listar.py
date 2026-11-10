"""Ventana: Listar agentes de navegación (grilla PAGINADA).

Muestra TODOS los atributos del agente de navegacion + 2 atributos del agente
inteligente (nombre y estado), con las consultas personalizadas navegacionesConAgente
(filtro por destino) y navegacionesPorAgente (filtro por agente inteligente).
"""
from vistas.agente_navegacion.comun import ConfigAgenteNavegacion
from vistas.casos_base import VentanaListar


class VistaListarAgenteNavegacion(ConfigAgenteNavegacion, VentanaListar):
    columnas = [
        ("idNavegacion", "ID", 60, "entero"),
        ("nombre", "Nombre", 120, "texto"),
        ("origen", "Origen", 100, "texto"),
        ("destino", "Destino", 100, "texto"),
        ("precisionGPS", "Precisión GPS %", 110, "decimal"),
        ("velocidadMaxima", "Vel. máx. km/h", 105, "decimal"),
        ("fechaUltimaCalibracion", "Última calibración", 135, "fecha"),
        ("rutaOptimizada", "Ruta optimizada", 110, "booleano"),
        ("idAgenteInteligente", "ID agente", 75, "referencia"),
        ("nombreAgente", "Agente inteligente", 130, "texto"),
        ("estadoAgente", "Estado del agente", 125, "texto"),
    ]
    filtros = [
        {"clave": None, "etiqueta": "Todos", "tipo": None},
        {"clave": "destino", "etiqueta": "Destino", "tipo": "texto"},
        {"clave": "agente", "etiqueta": "Agente inteligente", "tipo": "referencia"},
    ]

    def consultar(self, clave_filtro, valor, pagina, tamano):
        if clave_filtro == "destino":
            return self.servicio.listar_por_destino(valor, pagina, tamano)
        if clave_filtro == "agente":
            return self.servicio.listar_por_agente(valor, pagina, tamano)
        return self.servicio.listar_por_destino("", pagina, tamano)
