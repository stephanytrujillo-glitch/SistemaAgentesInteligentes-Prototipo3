"""Ventana: Listar agentes inteligentes (grilla PAGINADA + filtro por estado operativo).

Usa la consulta personalizada agentesInteligentesResumen: datos del maestro
+ 2 datos del detalle (cantidad de navegaciones y precision GPS promedio).
"""
from modelo.campos import ESTADOS_OPERATIVOS
from vistas.agente_inteligente.comun import ConfigAgenteInteligente
from vistas.casos_base import VentanaListar


class VistaListarAgenteInteligente(ConfigAgenteInteligente, VentanaListar):
    columnas = [
        ("idAgente", "ID", 60, "entero"),
        ("nombre", "Nombre", 130, "texto"),
        ("nivelAutonomia", "Autonomía %", 95, "decimal"),
        ("estadoOperativo", "Estado", 115, "texto"),
        ("nivelConfianza", "Confianza %", 95, "decimal"),
        ("fechaRegistro", "Registro", 130, "fecha"),
        ("aprendizajeContinuo", "Aprendizaje", 90, "booleano"),
        ("descripcion", "Descripción", 200, "texto"),
        ("cantidadNavegaciones", "N.º navegaciones", 115, "entero"),
        ("precisionPromedio", "Precisión GPS prom.", 130, "decimal"),
    ]
    filtros = [
        {"clave": None, "etiqueta": "Todos", "tipo": None},
        {"clave": "estado", "etiqueta": "Estado operativo", "tipo": "opcion", "opciones": ESTADOS_OPERATIVOS},
    ]

    def consultar(self, clave_filtro, valor, pagina, tamano):
        estado = valor if clave_filtro == "estado" else None
        return self.servicio.listar(estado, pagina, tamano)
