"""Formato de valores para mostrarlos al usuario."""


def formatear(tipo: str, valor) -> str:
    if tipo == "referencia" and valor is None:
        return "(sin asignar)"
    if valor is None or valor == "":
        return "—"
    if tipo == "booleano":
        return "Sí" if valor else "No"
    if tipo == "fecha":
        return str(valor).replace("T", " ")[:16]
    if tipo == "decimal":
        try:
            return f"{float(valor):.2f}"
        except (TypeError, ValueError):
            return str(valor)
    return str(valor)
