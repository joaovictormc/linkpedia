import math
from sqlite3 import DatabaseError
from fastapi import APIRouter, HTTPException, Query, Request, status, Form
from fastapi.responses import HTMLResponse, JSONResponse

from dtos.alterar_senha_dto import AlterarSenhaDTO
from dtos.login_dto import LoginDTO

# from dtos.novo_cliente_dto import NovoClienteDTO
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo

from util.auth import (
    conferir_senha,
    gerar_token,
    obter_hash_senha,
)

from util.cookies import adicionar_cookie_auth, adicionar_mensagem_erro, adicionar_mensagem_sucesso
from util.html import ler_html
from util.pydantic import create_validation_errors


from fastapi import APIRouter, Request

from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")


# @router.get("/")
# async def get_root(request: Request):
    
#     return templates.TemplateResponse(
#         "pages/index.html",
#         {
#             "request": request
#         },
#     )

@router.get("/html/{arquivo}")
async def get_html(arquivo: str):
    response = HTMLResponse(ler_html(arquivo))
    return response

@router.get("/", response_class=HTMLResponse)
async def get_entrar(
    request: Request,
    return_url: str = Query("/"),
):
    return templates.TemplateResponse(
        "pages/login/login.html",
        {
            "request": request,
            "return_url": return_url,
        },
    )


@router.get("/cadastrar")
async def get_cadastrar(request: Request):
    return templates.TemplateResponse(
        "pages/login/cadastrar.html",
        {"request": request},
    )


# @router.get("/recuperarsenha")
# async def get_recuperarsenha(request: Request):
#     return templates.TemplateResponse(
#         "pages/login/recuperarSenha.html",
#         {"request": request},
#     )

@router.get("/favoritos", response_class=HTMLResponse)
async def get_favoritos(request: Request):
    return templates.TemplateResponse(
        "pages/favorito/favoritos.html",
        {"request": request},
    )


@router.post("/post_login", response_class=JSONResponse)
async def post_entrar(request: Request, email: str = Form(...), password: str = Form(...)):
    usuario_entrou = UsuarioRepo.obter_por_email(email)
    if not usuario_entrou or not usuario_entrou.senha or not conferir_senha(password, usuario_entrou.senha):
        return JSONResponse(
            content=create_validation_errors({"email": email, "senha": password}, ["email", "senha"], ["Credenciais inválidas.", "Credenciais inválidas."]),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    token = gerar_token()
    if not UsuarioRepo.alterar_token(usuario_entrou.id, token):
        raise DatabaseError("Não foi possível alterar o token do usuário no banco de dados.")
    response = JSONResponse(content={"redirect": {"url": "/favoritos"}})
    adicionar_mensagem_sucesso(response, f"Olá, <b>{usuario_entrou.nome}</b>. Seja bem-vindo(a) à Loja Virtual!")
    adicionar_cookie_auth(response, token)
    request.state.usuario = usuario_entrou  # Adiciona o usuário ao estado da requisição
    return response

@router.post("/post_senha", response_class=JSONResponse)
async def post_senha(request: Request, alterar_dto: AlterarSenhaDTO):
    email = request.state.usuario.email
    usuario_bd = UsuarioRepo.obter_por_email(email)
    nova_senha_hash = obter_hash_senha(alterar_dto.nova_senha)
    response = JSONResponse({"redirect": {"url": "/usuario/recuperarSenha"}})
    if not conferir_senha(alterar_dto.senha, usuario_bd.senha):
        adicionar_mensagem_erro(response, "Senha atual incorreta!")
        return response
    if UsuarioRepo.alterar_senha(usuario_bd.id, nova_senha_hash):
        adicionar_mensagem_sucesso(response, "Senha alterada com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível alterar sua senha!")
    return response

# @router.post("/post_cadastro", response_class=JSONResponse)
# async def post_cadastro(cliente_dto: NovoClienteDTO):
#     usuario_data = cliente_dto.model_dump(exclude={"confirmacao_senha"})
#     usuario_data["senha"] = obter_hash_senha(usuario_data["senha"])
#     novo_cliente = UsuarioRepo.inserir(Usuario(**usuario_data))
#     if not novo_cliente or not novo_cliente.id:
#         raise HTTPException(status_code=400, detail="Erro ao cadastrar cliente.")
#     return {"redirect": {"url": "/cadastro_realizado"}}


# @router.get("/cadastro_realizado")
# async def get_cadastro_realizado(request: Request):
#     return templates.TemplateResponse(
#         "pages/cadastro_confirmado.html",
#         {"request": request},
#     )

