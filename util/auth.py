import secrets
from typing import Optional
import bcrypt
from fastapi import HTTPException, Request, status
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.cookies import NOME_COOKIE_AUTH, adicionar_cookie_auth

async def obter_usuario_logado(request: Request) -> Optional[Usuario]:
    try:
        token = request.cookies.get(NOME_COOKIE_AUTH, "").strip()
        if not token:
            return None
        return UsuarioRepo.obter_por_token(token)
    except KeyError:
        return None

async def middleware_autenticacao(request: Request, call_next):
    usuario = await obter_usuario_logado(request)
    request.state.usuario = usuario
    response = await call_next(request)
    if response.status_code == status.HTTP_303_SEE_OTHER:
        return response
    if usuario:
        token = request.cookies.get(NOME_COOKIE_AUTH)
        adicionar_cookie_auth(response, token)
    return response

async def checar_permissao(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    area_do_usuario = request.url.path.startswith("/favoritos")
    if area_do_usuario and not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

def obter_hash_senha(senha: str) -> str:
    try:
        hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        return hashed.decode()
    except ValueError:
        return ""

def conferir_senha(senha: str, hash_senha: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    except ValueError:
        return False

def gerar_token(length: int = 32) -> str:
    try:
        return secrets.token_hex(length)
    except ValueError:
        return ""
