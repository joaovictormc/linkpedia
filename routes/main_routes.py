import math
from sqlite3 import DatabaseError
from fastapi import APIRouter, HTTPException, Query, Request, status, Form
from fastapi.responses import HTMLResponse, JSONResponse

from dtos.alterar_senha_dto import AlterarSenhaDTO
from dtos.login_dto import LoginDTO
from dtos.novo_usuario_dto import NovoUsuarioDTO

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

# Rotas de cadastros ##########################################
@router.get("/cadastrar")
async def get_cadastrar(request: Request):
    return templates.TemplateResponse(
        "pages/login/cadastrar.html",
        {"request": request},
    )
    
@router.post("/post_cadastro", response_class=JSONResponse)
async def post_cadastro(usuario_dto: NovoUsuarioDTO):
    usuario_data = usuario_dto.model_dump(exclude={"confirmacao_senha"})
    usuario_data["senha"] = obter_hash_senha(usuario_data["senha"])
    novo_usuario = UsuarioRepo.inserir(Usuario(**usuario_data))
    
    if not novo_usuario or not novo_usuario.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar usuário.")
    return {"redirect": {"url": "/cadastro_realizado"}}


@router.get("/cadastro_realizado")
async def get_cadastro_realizado(request: Request):
    return templates.TemplateResponse(
        "pages/login/cadastro_realizado.html",
        {"request": request},
    )

################################################################

# Rotas de Recuperação de senha ##########################################

@router.get("/recuperar_senha")
async def get_cadastrar(request: Request):
    return templates.TemplateResponse(
        "pages/login/recuperar_senha.html",
        {"request": request},
    )
    
@router.get("/senha_alterada")
async def get_cadastrar(request: Request):
    return templates.TemplateResponse(
        "pages/login/senha_alterada.html",
        {"request": request},
    )
    
##########################################################################
    


@router.get("/favoritos", response_class=HTMLResponse)
async def get_favoritos(request: Request):
    return templates.TemplateResponse(
        "pages/favorito/favoritos.html",
        {"request": request},
    )


@router.post("/post_login", response_class=JSONResponse)
async def post_login(login_dto: LoginDTO):
    usuario_entrou = UsuarioRepo.obter_por_email(login_dto.email)
    if (
        (not usuario_entrou)
        or (not usuario_entrou.senha)
        or (not conferir_senha(login_dto.senha, usuario_entrou.senha))
    ):
        return JSONResponse(content={"detail": create_validation_errors(
                login_dto,
                ["email", "senha"],
                ["Credenciais inválidas.", "Credenciais inválidas."],
            )})
  
    token = gerar_token()
    if not UsuarioRepo.alterar_token(usuario_entrou.id, token):
        raise HTTPException(status_code=400, detail="Não foi possível alterar o token do usuário no banco de dados.")  
    
    response = JSONResponse(content={"redirect": {"url": "/favoritos"}})
    adicionar_cookie_auth(response, token)
    return response


