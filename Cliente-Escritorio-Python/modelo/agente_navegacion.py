"""Clase estructural AgenteNavegacion (detalle) del lado del cliente."""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class AgenteNavegacion:
    idNavegacion: int
    nombre: str
    origen: str
    destino: str
    precisionGPS: float
    velocidadMaxima: Optional[float]
    fechaUltimaCalibracion: str
    rutaOptimizada: bool
    idAgenteInteligente: Optional[int] = None

    @classmethod
    def desde_dict(cls, datos: dict) -> "AgenteNavegacion":
        return cls(
            idNavegacion=datos["idNavegacion"],
            nombre=datos["nombre"],
            origen=datos["origen"],
            destino=datos["destino"],
            precisionGPS=datos["precisionGPS"],
            velocidadMaxima=datos.get("velocidadMaxima"),
            fechaUltimaCalibracion=datos["fechaUltimaCalibracion"],
            rutaOptimizada=datos["rutaOptimizada"],
            idAgenteInteligente=datos.get("idAgenteInteligente"),
        )

    def como_dict(self) -> dict:
        return asdict(self)

    def __str__(self):
        return f"{self.idNavegacion} - {self.nombre}"
