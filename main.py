from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles


from routes import main_routes


app = FastAPI()

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

app.include_router(main_routes.router)

