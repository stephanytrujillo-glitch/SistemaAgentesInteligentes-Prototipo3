"""Validacion y conversion de los datos digitados por el usuario antes de enviarlos al servidor."""
import re
from datetime import datetime

FORMATOS_FECHA = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"]


class ErrorValidacion(Exception):
    """Agrupa todos los errores de validacion de un formulario."""

    def __init__(self, errores):
        self.errores = errores
        super().__init__("\n".join(errores))


def convertir_fecha(texto: str) -> datetime:
    for formato in FORMATOS_FECHA:
        try:
            return datetime.strptime(texto.strip(), formato)
        except ValueError:
            continue
    raise ValueError("formato")


def _numero(texto, entero):
    texto = texto.strip().replace(",", ".")
    return int(texto) if entero else float(texto)


def validar(campos, valores: dict, incluir_llave: bool = True) -> dict:
    """Valida 'valores' (crudos del formulario) contra la definicion de 'campos'.

    Devuelve un dict listo para enviar como input GraphQL o lanza ErrorValidacion.
    """
    errores = []
    datos = {}

    for campo in campos:
        if campo.es_llave and not incluir_llave:
            continue
        valor = valores.get(campo.clave)
        nombre = campo.etiqueta

        if campo.tipo == "booleano":
            datos[campo.clave] = bool(valor)
            continue

        if campo.tipo == "referencia":
            if isinstance(valor, str):  # texto escrito que no corresponde a ningun agente
                errores.append(f"{nombre}: escriba el nombre o el ID y elija un agente de la lista.")
                continue
            datos[campo.clave] = valor  # int o None (ya convertido por el formulario)
            if valor is None and campo.obligatorio:
                errores.append(f"{nombre} es obligatorio.")
            continue

        texto = "" if valor is None else str(valor).strip()
        if texto == "":
            if campo.obligatorio:
                errores.append(f"{nombre} es obligatorio.")
            datos[campo.clave] = None
            continue

        if campo.tipo in ("entero", "decimal"):
            try:
                numero = _numero(texto, campo.tipo == "entero")
            except ValueError:
                tipo = "un número entero" if campo.tipo == "entero" else "un número"
                errores.append(f"{nombre} debe ser {tipo}.")
                continue
            if campo.minimo is not None:
                if campo.minimo_exclusivo and numero <= campo.minimo:
                    errores.append(f"{nombre} debe ser mayor que {campo.minimo}.")
                    continue
                if not campo.minimo_exclusivo and numero < campo.minimo:
                    errores.append(f"{nombre} debe ser mayor o igual a {campo.minimo}.")
                    continue
            if campo.maximo is not None and numero > campo.maximo:
                errores.append(f"{nombre} debe ser menor o igual a {campo.maximo}.")
                continue
            datos[campo.clave] = numero

        elif campo.tipo == "texto":
            if campo.min_largo and len(texto) < campo.min_largo:
                errores.append(f"{nombre} debe tener al menos {campo.min_largo} caracteres.")
                continue
            if campo.max_largo and len(texto) > campo.max_largo:
                errores.append(f"{nombre} admite máximo {campo.max_largo} caracteres.")
                continue
            if campo.patron and not re.match(campo.patron, texto):
                errores.append(f"{nombre} solo admite letras, números, espacios, punto, guion y guion bajo.")
                continue
            datos[campo.clave] = texto

        elif campo.tipo == "fecha":
            try:
                fecha = convertir_fecha(texto)
            except ValueError:
                errores.append(f"{nombre} debe tener el formato AAAA-MM-DD HH:MM.")
                continue
            if fecha > datetime.now():
                errores.append(f"{nombre} no puede ser una fecha futura.")
                continue
            datos[campo.clave] = fecha.strftime("%Y-%m-%dT%H:%M:%S")

        elif campo.tipo == "opcion":
            if texto not in campo.opciones:
                errores.append(f"{nombre} debe ser uno de: {', '.join(campo.opciones)}.")
                continue
            datos[campo.clave] = texto

    # Regla de negocio entre atributos
    if datos.get("origen") and datos.get("destino") and datos["origen"].lower() == datos["destino"].lower():
        errores.append("El origen y el destino deben ser diferentes.")

    if errores:
        raise ErrorValidacion(errores)
    return datos
