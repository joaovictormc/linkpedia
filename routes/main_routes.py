
from fastapi import APIRouter, Request

from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")


@router.get("/")
async def get_root(request: Request):
    
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request
        },
    )


