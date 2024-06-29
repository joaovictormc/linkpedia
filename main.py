from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from repositories.categoria_repo import CategoriaRepo
from repositories.favorito_repo import FavoritoRepo
from repositories.usuario_repo import UsuarioRepo
from routes import main_routes, favorito_routes
from util.auth import checar_permissao, middleware_autenticacao
from util.exceptions import configurar_excecoes


from routes import main_routes

FavoritoRepo.criar_tabela()
CategoriaRepo.criar_tabela()
CategoriaRepo.inserir_categoria_json("sql/categoria.json")
UsuarioRepo.criar_tabela()
UsuarioRepo.inserir_usuarios_json("sql/usuarios.json")

app = FastAPI(dependencies=[Depends(checar_permissao)])
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.middleware(middleware_type="http")(middleware_autenticacao)
configurar_excecoes(app)

app.include_router(main_routes.router)
app.include_router(favorito_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")