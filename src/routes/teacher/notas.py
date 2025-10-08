from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.schemas.teacher.notas import  NotaBase, NotasGroupOut, NotaUpdate
from src.core.security import get_current_user, get_current_teacher
from src.services.teacher.notas import listar_notas, criar_notas, editar_nota, excluir_nota
from src.models.user_model import User

router = APIRouter(
    prefix="/teacher/notas",
    tags=["Professor - Notas"]
)

@router.get("/", response_model=List[NotasGroupOut])
def listar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    return listar_notas(db, current_user.email)

@router.post("/", response_model=List[NotasGroupOut],status_code=status.HTTP_201_CREATED)
def criar(
    nota_in: NotaBase, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_teacher)):
    try:
        return criar_notas(db, nota_in, current_user.email)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{nota_id}", response_model=NotasGroupOut)
def editar(
    nota_id: int,
    nota_update: NotaUpdate,
    db: Session = Depends(get_db),               # sessão do banco
    current_user: User = Depends(get_current_teacher)  # professor logado
):
    try:
        grupo = editar_nota(db, nota_id, nota_update, current_user.email)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not grupo:
        raise HTTPException(status_code=404, detail="Tarefa/nota não encontrada")
    return grupo

@router.delete("/{nota_id}")
def excluir(nota_id: int, 
            db: Session = Depends(get_db),
            current_teacher: User = Depends(get_current_teacher)):
    nota = excluir_nota(db, nota_id, current_teacher)
    if not nota:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    return {"message": "Chamada excluída com sucesso"}
