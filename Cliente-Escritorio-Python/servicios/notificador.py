"""Patron Observer: avisa a las ventanas suscritas cuando cambian los datos de una clase.

Ejemplo: si la ventana Listar esta abierta y en otra ventana se adiciona, actualiza o
elimina un registro, la grilla se refresca sola.
"""

AGENTE_INTELIGENTE = "agente_inteligente"
AGENTE_NAVEGACION = "agente_navegacion"


class Notificador:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._observadores = {}
        return cls._instancia

    def suscribir(self, evento: str, observador):
        self._observadores.setdefault(evento, []).append(observador)

    def desuscribir(self, evento: str, observador):
        if observador in self._observadores.get(evento, []):
            self._observadores[evento].remove(observador)

    def notificar(self, evento: str):
        for observador in list(self._observadores.get(evento, [])):
            try:
                observador(evento)
            except Exception:  # noqa: BLE001 - un observador con error no detiene a los demas
                pass
