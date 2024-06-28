from pydantic import BaseModel, field_validator

from util.validators import *


class AlterarSenhaDTO(BaseModel):
    senha: str
    nova_senha: str

    @field_validator("senha")
    def validar_senha(cls, v):
        msg = is_not_empty(v, "Senha")
        if not msg:
            msg = is_password(v, "Senha")
        if msg:
            raise ValueError(msg.strip())
        return v

    @field_validator("nova_senha")
    def validar_nova_senha(cls, v):
        msg = is_not_empty(v, "Nova Senha")
        if not msg:
            msg = is_password(v, "Nova Senha")
        if msg:
            raise ValueError(msg.strip())
        return v

    