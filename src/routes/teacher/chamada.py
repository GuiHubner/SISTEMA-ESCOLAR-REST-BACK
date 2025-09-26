from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.schemas.teacher.chamada import  ChamadaOut, ChamadaBase, ChamadaUpdate
from src.core.security import get_current_user, get_current_teacher
from src.services.teacher.chamada import criar_chamada, listar_chamadas, editar_chamada, excluir_chamada
from src.models.user_model import User

router = APIRouter(
    prefix="/teacher/chamada",
    tags=["Professor - Chamada"]
)

@router.get("/", response_model=List[ChamadaOut])
def listar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    return listar_chamadas(db, current_user.email)

@router.post("/", response_model=ChamadaOut)
def criar(
    chamada: ChamadaBase, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_teacher)):
    return criar_chamada(db, chamada, current_user.email)

@router.put("/{chamada_id}", response_model=ChamadaOut)
def editar(
    chamada_id: int,
    chamada_update: ChamadaUpdate,
    db: Session = Depends(get_db),               # sessão do banco
    current_teacher: User = Depends(get_current_teacher)  # professor logado
):
    chamada = editar_chamada(db, chamada_id, chamada_update, current_teacher)
    if not chamada:
        raise HTTPException(status_code=404, detail="Chamada não encontrada")
    return chamada

@router.delete("/{chamada_id}")
def excluir(chamada_id: int, 
            db: Session = Depends(get_current_teacher)):
    chamada = excluir_chamada(db, chamada_id)
    if not chamada:
        raise HTTPException(status_code=404, detail="Chamada não encontrada")
    return {"message": "Chamada excluída com sucesso"}
