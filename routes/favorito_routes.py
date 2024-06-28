from sqlite3 import DatabaseError
from fastapi import APIRouter, HTTPException, Request, status, Form
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
from models.favorito_model import Favorito
from repositories.favorito_repo import FavoritoRepo

from util.templates import obter_jinja_templates

router = APIRouter(prefix="/favorito")
templates = obter_jinja_templates("templates/favorito")

@router.get("/index", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse(
        "pages/favorito/favoritos.html",
        {
            "request": request
        },
    )

# Rota para adicionar um favorito
@router.post("/add", response_class=JSONResponse)
async def add_favorito(request: Request, id_link: int = Form(...)):
    try:
        id_usuario = request.state.usuario.id  # Assumindo que o usuário está no estado da requisição
        novo_favorito = Favorito(id_usuario=id_usuario, id_link=id_link)
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
async def list_favoritos(request: Request):
    try:
        id_usuario = request.state.usuario.id  # Assumindo que o usuário está no estado da requisição
        favoritos = FavoritoRepo.obter_todos()
        favoritos_usuario = [f for f in favoritos if f.id_usuario == id_usuario]
        return JSONResponse(content=favoritos_usuario, status_code=status.HTTP_200_OK)
    except DatabaseError as e:
        return JSONResponse(
            content={"message": f"Erro ao listar favoritos: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

# Rota para a página principal de favoritos
@router.get("/", response_class=HTMLResponse)
async def get_favoritos(request: Request):
    return templates.TemplateResponse(
        "pages/favorito/favoritos.html",
        {"request": request},
    )
