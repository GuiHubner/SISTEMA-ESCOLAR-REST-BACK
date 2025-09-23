from fastapi import FastAPI
from src.database import Base, engine
from src.routes.teacher import tasks

from fastapi import FastAPI
from src.database import Base, engine
from src.routes import auth

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Escolar com Autenticação")

# Rotas
app.include_router(auth.router)
app.include_router(tasks.router)
