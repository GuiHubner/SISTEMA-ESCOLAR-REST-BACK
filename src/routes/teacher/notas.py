from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.schemas.teacher.notas import NotaOut, NotaBase
from src.core.security import get_current_user, get_current_teacher
from src.services.teacher.notas import listar_notas, criar_notas
from src.models.user_model import User

router = APIRouter(
    prefix="/teacher/notas",
    tags=["Professor - Notas"]
)

@router.get("/", response_model=List[NotaOut])
def listar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    return listar_notas(db, current_user.email)

@router.post("/", response_model=List[NotaOut])
def criar(
    notas: NotaBase, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_teacher)):
    return criar_notas(db, notas, current_user.email)

# @router.put("/{chamada_id}", response_model=ChamadaOut)
# def editar(
#     chamada_id: int,
#     chamada_update: ChamadaUpdate,
#     db: Session = Depends(get_db),               # sessão do banco
#     current_teacher: User = Depends(get_current_teacher)  # professor logado
# ):
#     chamada = editar_chamada(db, chamada_id, chamada_update, current_teacher)
#     if not chamada:
#         raise HTTPException(status_code=404, detail="Chamada não encontrada")
#     return chamada

# @router.delete("/{chamada_id}")
# def excluir(chamada_id: int, 
#             db: Session = Depends(get_db),
#             current_teacher: User = Depends(get_current_teacher)):
#     chamada = excluir_chamada(db, chamada_id, current_teacher)
#     if not chamada:
#         raise HTTPException(status_code=404, detail="Chamada não encontrada")
#     return {"message": "Chamada excluída com sucesso"}
