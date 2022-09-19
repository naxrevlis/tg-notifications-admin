from tokenize import Token
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from tortoise import Tortoise
from fastapi.middleware.cors import CORSMiddleware


from database.register import register_tortoise
from database.config import TORTOISE_ORM

Tortoise.init_models(["database.models"], "models")

from routes import users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return str(context)


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
