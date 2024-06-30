from sqlite3 import DatabaseError
from fastapi import APIRouter, HTTPException, Request, status, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import List
from dtos.novo_usuario_dto import NovoUsuarioDTO
from models.categoria_model import Categoria
from models.favorito_model import Favorito
from models.usuario_model import Usuario
from repositories.categoria_repo import CategoriaRepo
from repositories.favorito_repo import FavoritoRepo

from repositories.usuario_repo import UsuarioRepo
from util.auth import obter_hash_senha
from util.cookies import adicionar_mensagem_sucesso, excluir_cookie_auth
from util.templates import obter_jinja_templates

router = APIRouter(prefix="/favorito")
templates = obter_jinja_templates("templates/main")

# @router.get("/index", response_class=HTMLResponse)
# async def get_index(request: Request):
#     return templates.TemplateResponse(
#         "pages/favorito/favoritos.html",
#         {
#             "request": request
#         },
#     )

# Rota para adicionar um favorito
@router.post("/add", response_class=JSONResponse)
async def add_favorito(request: Request, nome: str = Form(...), url: str = Form(...), id_categoria: str = Form(...), id_usuario: int = Form(None)):
    try:
    
        novo_favorito = Favorito(id_usuario=id_usuario, nome=nome, id_categoria=id_categoria, url=url)
        FavoritoRepo.inserir(novo_favorito)
        return JSONResponse(
            content={"message": "Favorito adicionado com sucesso!"},
            status_code=status.HTTP_201_CREATED,
        )
    except DatabaseError as e:
        return JSONResponse(
            content={"message": f"Erro ao adicionar favorito: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
@router.post("/update", response_class=JSONResponse)
async def update_categoria(request: Request,id:str=Form(...), nome: str = Form(...), url: str = Form(...), id_categoria: str = Form(...), id_usuario: int = Form(None)):
    try:
        favorito = Favorito(id=id, id_usuario=id_usuario, nome=nome, id_categoria=id_categoria, url=url)
        FavoritoRepo.alterar(favorito)
        return JSONResponse(
            content={"message": "Favorito atualizada com sucesso!"},
            status_code=status.HTTP_200_OK,
        )
    except DatabaseError as e:
        return JSONResponse(
            content={"message": f"Erro ao atualizar o favorito: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
# Rota para remover um favorito
@router.post("/remove", response_class=JSONResponse)
async def remove_favorito(request: Request, id: int = Form(...)):
    try:
        FavoritoRepo.excluir(id)
        return JSONResponse(
            content={"message": "Favorito removido com sucesso!"},
            status_code=status.HTTP_200_OK,
        )
    except DatabaseError as e:
        return JSONResponse(
            content={"message": f"Erro ao remover favorito: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

# Rota para listar todos os favoritos do usuário
@router.get("/list", response_class=JSONResponse)
async def list_favoritos(request: Request, id_usuario: int, id_categoria: int = None, filter: str = None):
    try:

        favoritos = FavoritoRepo.obter_todos()
        # Filtrando por usuário
        favoritos_usuario = [f for f in favoritos if f.id_usuario == id_usuario]

        # Filtrando por categoria, se fornecida
        if id_categoria is not None:
            favoritos_usuario = [f for f in favoritos_usuario if f.id_categoria == id_categoria]
        
        # Aplicando filtro de texto, se fornecido
        if filter:
            filter = filter.lower()
            favoritos_usuario = [f for f in favoritos_usuario if filter in f.nome.lower() or filter in f.url.lower()]
        
        favoritos_dict = [{"id": fav.id, "nome": fav.nome, "url": fav.url, "id_categoria": fav.id_categoria, "id_usuario": fav.id_usuario} for fav in favoritos_usuario]

        return JSONResponse(content=favoritos_dict, status_code=status.HTTP_200_OK)
    except DatabaseError as e:
        return JSONResponse(
            content={"message": f"Erro ao listar favoritos: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/sair", response_class=RedirectResponse)
async def get_sair(request: Request):
    if request.state.favorito:
        FavoritoRepo.alterar_token(request.state.favorito.email, "")
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    excluir_cookie_auth(response)
    adicionar_mensagem_sucesso(response, "Saída realizada com sucesso!")
    return response


@router.post("/categoria/add", response_class=JSONResponse)
async def add_categoria(request: Request, nome: str = Form(...), icone: str = Form(None)):
    try:
        nova_categoria = Categoria(nome=nome, icone=icone)
        CategoriaRepo.inserir(nova_categoria)
        return JSONResponse(
            content={"message": "Categoria adicionada com sucesso!"},
            status_code=status.HTTP_201_CREATED,
        )
    except DatabaseError as e:
        return JSONResponse(
            content={"message": f"Erro ao adicionar categoria: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

@router.post("/categoria/update", response_class=JSONResponse)
async def update_categoria(request: Request, id: int = Form(...), nome: str = Form(...), icone: str = Form(None)):
    try:
        categoria = Categoria(id=id, nome=nome, icone=icone)
        CategoriaRepo.alterar(categoria)
        return JSONResponse(
            content={"message": "Categoria atualizada com sucesso!"},
            status_code=status.HTTP_200_OK,
        )
    except DatabaseError as e:
        return JSONResponse(
            content={"message": f"Erro ao atualizar categoria: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
@router.get("/categoria/list", response_class=JSONResponse)
async def list_categorias(request: Request):
    try:
        categorias = CategoriaRepo.obter_todos()
        categorias_dict = [{"id": cat.id, "nome": cat.nome, "icone": cat.icone} for cat in categorias]

        return JSONResponse(content=categorias_dict, status_code=status.HTTP_200_OK)
    except DatabaseError as e:
        return JSONResponse(
            content={"message": f"Erro ao listar categorias: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

@router.get("/sobre", response_class=HTMLResponse)
async def get_sobre(request: Request):
    return templates.TemplateResponse(
        "pages/favorito/sobre.html",
        {
            "request": request
        },
    )

@router.post("/categoria/remover", response_class=JSONResponse)
async def remover_categoria(request: Request, id: int = Form(...)):
    try:
        CategoriaRepo.excluir(id)
        return JSONResponse(
            content={"message": "Caregoria removida com sucesso!"},
            status_code=status.HTTP_200_OK,
        )
    except DatabaseError as e:
        return JSONResponse(
            content={"message": f"Erro ao remover a categoria: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    

@router.get("/perfil")
async def get_perfil(request: Request):
    return templates.TemplateResponse(
        "pages/favorito/perfil.html",
        {"request": request},
    )


@router.post("/post_perfil", response_class=JSONResponse)
async def post_perfil(usuario_dto: NovoUsuarioDTO):
    usuario_data = usuario_dto.model_dump(exclude={"confirmacao_senha"})
    usuario_data["senha"] = obter_hash_senha(usuario_data["senha"])
    novo_usuario = UsuarioRepo.alterar(Usuario(**usuario_data))
    
    if not novo_usuario or not novo_usuario.id:
        raise HTTPException(status_code=400, detail="Erro ao atualizar o usuário.")
    return {"redirect": {"url": "/favorito"}}