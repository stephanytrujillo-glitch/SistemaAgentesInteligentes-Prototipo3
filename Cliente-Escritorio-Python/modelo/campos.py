"""Definicion de los atributos de cada clase: tipo, obligatoriedad y reglas de validacion."""

ESTADOS_OPERATIVOS = ["ACTIVO", "INACTIVO", "MANTENIMIENTO"]
PATRON_NOMBRE = r"^[A-Za-z0-9ÁÉÍÓÚáéíóúÑñÜü _.-]+$"


class Campo:
    """Describe un atributo de una clase del modelo para formularios, fichas y validaciones.

    tipos: entero, decimal, texto, fecha, booleano, opcion, referencia
    """

    def __init__(self, clave, etiqueta, tipo, obligatorio=True, minimo=None, maximo=None,
                 minimo_exclusivo=False, min_largo=None, max_largo=None, patron=None,
                 opciones=None, es_llave=False, ayuda=""):
        self.clave = clave
        self.etiqueta = etiqueta
        self.tipo = tipo
        self.obligatorio = obligatorio
        self.minimo = minimo
        self.maximo = maximo
        self.minimo_exclusivo = minimo_exclusivo
        self.min_largo = min_largo
        self.max_largo = max_largo
        self.patron = patron
        self.opciones = opciones or []
        self.es_llave = es_llave
        self.ayuda = ayuda


CAMPOS_AGENTE_INTELIGENTE = [
    Campo("idAgente", "ID del agente", "entero", minimo=1, es_llave=True, ayuda="Entero positivo, único"),
    Campo("nombre", "Nombre", "texto", min_largo=3, max_largo=50, patron=PATRON_NOMBRE,
          ayuda="3 a 50 caracteres, único"),
    Campo("nivelAutonomia", "Nivel de autonomía (%)", "decimal", minimo=0, maximo=100, ayuda="0 a 100"),
    Campo("estadoOperativo", "Estado operativo", "opcion", opciones=ESTADOS_OPERATIVOS),
    Campo("nivelConfianza", "Nivel de confianza (%)", "decimal", obligatorio=False, minimo=0, maximo=100,
          ayuda="Opcional, 0 a 100"),
    Campo("fechaRegistro", "Fecha de registro", "fecha", ayuda="AAAA-MM-DD HH:MM, no futura"),
    Campo("aprendizajeContinuo", "Aprendizaje continuo", "booleano"),
    Campo("descripcion", "Descripción", "texto", obligatorio=False, max_largo=200,
          ayuda="Opcional, máximo 200 caracteres"),
]

CAMPOS_AGENTE_NAVEGACION = [
    Campo("idNavegacion", "ID de navegación", "entero", minimo=1, es_llave=True, ayuda="Entero positivo, único"),
    Campo("nombre", "Nombre", "texto", min_largo=3, max_largo=50, patron=PATRON_NOMBRE,
          ayuda="3 a 50 caracteres, único"),
    Campo("origen", "Origen", "texto", min_largo=2, max_largo=60),
    Campo("destino", "Destino", "texto", min_largo=2, max_largo=60, ayuda="Diferente del origen"),
    Campo("precisionGPS", "Precisión GPS (%)", "decimal", minimo=0, maximo=100, ayuda="0 a 100"),
    Campo("velocidadMaxima", "Velocidad máxima (km/h)", "decimal", obligatorio=False, minimo=0,
          minimo_exclusivo=True, maximo=500, ayuda="Opcional, mayor que 0 y hasta 500"),
    Campo("fechaUltimaCalibracion", "Última calibración", "fecha", ayuda="AAAA-MM-DD HH:MM, no futura"),
    Campo("rutaOptimizada", "Ruta optimizada", "booleano"),
    Campo("idAgenteInteligente", "Agente inteligente asignado", "referencia", obligatorio=False,
          ayuda="Opcional. Escriba nombre o ID y despliegue la lista"),
]
