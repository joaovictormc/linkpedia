from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Favorito:
    id: Optional[int] = None
    nome: Optional[str] = None
    url: Optional[str] = None
    id_categoria: Optional[str] = None
    id_usuario: Optional[int] = None
