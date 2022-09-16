from tokenize import Token
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tortoise import Tortoise

from database.register import register_tortoise
from database.config import TORTOISE_ORM

Tortoise.init_models(["database.models"], "models")


from routes import users


app = FastAPI()

app.include_router(users.router)

templates = Jinja2Templates(directory="templates")

print(TORTOISE_ORM)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


# @app.post("/token/post", response_class=HTMLResponse)
# async def post_token(token: Token):
#     token_id = await DB.append(token)
#     return str({"id": token_id})
    

# @app.get("/token/get", response_class=HTMLResponse)
# async def get_token(id: int):
#     try:
#         return await DB.token[id]
#     except Exception as e:
#         return {"status": "error", "message": str(e)}