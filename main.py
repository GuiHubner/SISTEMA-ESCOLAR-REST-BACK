from fastapi import FastAPI
from src.database import Base, engine
from src.routes.teacher import tasks, chamada, notas

from fastapi import FastAPI
from src.database import Base, engine
from src.routes import auth

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Escolar com Autenticação")

# Rotas
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chamada.router)
app.include_router(notas.router)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",        # <nome_do_arquivo>:<nome_da_instância_FastAPI>
        host="127.0.0.1",  # ou "0.0.0.0" se quiser expor na rede
        port=8000,
        reload=True        # recarrega automaticamente quando salvar alterações
    )
