"""Configuracion general del cliente de escritorio."""
import os

# URL del servidor GraphQL (se puede cambiar con la variable de entorno GRAPHQL_URL)
URL_GRAPHQL = os.environ.get("GRAPHQL_URL", "http://localhost:8081/graphql")

NOMBRE_APP = "Sistema de Agentes Inteligentes"
VERSION = "3.0.0"
TECNOLOGIA = "Cliente de escritorio - Python 3 + Tkinter"
CURSO = "Desarrollo de Aplicaciones Empresariales - Universidad de Ibague - 2026B"

# Nombre que aparece en Ayuda > Acerca de...
INTEGRANTES = [
    "Stephany Trujillo Murillo",
]
