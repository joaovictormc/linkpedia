from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Categoria:
    id: Optional[int] = None
    nome: Optional[str] = None
    icone: Optional[str] = None
