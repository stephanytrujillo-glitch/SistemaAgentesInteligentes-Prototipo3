"""Clase estructural AgenteInteligente (maestro) del lado del cliente."""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class AgenteInteligente:
    idAgente: int
    nombre: str
    nivelAutonomia: float
    estadoOperativo: str
    nivelConfianza: Optional[float]
    fechaRegistro: str
    aprendizajeContinuo: bool
    descripcion: Optional[str] = None

    @classmethod
    def desde_dict(cls, datos: dict) -> "AgenteInteligente":
        return cls(
            idAgente=datos["idAgente"],
            nombre=datos["nombre"],
            nivelAutonomia=datos["nivelAutonomia"],
            estadoOperativo=datos["estadoOperativo"],
            nivelConfianza=datos.get("nivelConfianza"),
            fechaRegistro=datos["fechaRegistro"],
            aprendizajeContinuo=datos["aprendizajeContinuo"],
            descripcion=datos.get("descripcion"),
        )

    def como_dict(self) -> dict:
        return asdict(self)

    def __str__(self):
        return f"{self.idAgente} - {self.nombre}"
