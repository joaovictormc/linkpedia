import math
from sqlite3 import DatabaseError
from fastapi import APIRouter, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse

from dtos.login_dto import LoginDTO

# from dtos.novo_cliente_dto import NovoClienteDTO
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo

from util.auth import (
    conferir_senha,
    gerar_token,
    obter_hash_senha,
)

from util.cookies import adicionar_cookie_auth, adicionar_mensagem_sucesso
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



@router.get("/")
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

@router.post("/post_login", response_class=JSONResponse)
async def post_entrar(login_dto: LoginDTO):
    usuario_entrou = UsuarioRepo.obter_por_email(login_dto.email)
    if (
        (not usuario_entrou)
        or (not usuario_entrou.senha)
        or (not conferir_senha(login_dto.senha, usuario_entrou.senha))
    ):
        return JSONResponse(
            content=create_validation_errors(
                login_dto,
                ["email", "senha"],
                ["Credenciais inválidas.", "Credenciais inválidas."],
            ),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    token = gerar_token()
    if not UsuarioRepo.alterar_token(usuario_entrou.id, token):
        raise DatabaseError(
            "Não foi possível alterar o token do usuário no banco de dados."
        )
    response = JSONResponse(content={"redirect": {"url": login_dto.return_url}})
    adicionar_mensagem_sucesso(
        response,
        f"Olá, <b>{usuario_entrou.nome}</b>. Seja bem-vindo(a) à Loja Virtual!",
    )
    adicionar_cookie_auth(response, token)
    return response


@router.get("/cadastrar")
async def get_cadastrar(request: Request):
    return templates.TemplateResponse(
        "pages/login/cadastrar.html",
        {"request": request},
    )


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

