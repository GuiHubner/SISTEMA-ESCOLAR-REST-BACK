from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.schemas.teacher.chamada import  ChamadaOut, ChamadaBase
from src.core.security import get_current_user, get_current_teacher
from src.services.teacher.chamada import criar_chamada, listar_chamadas
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

# @router.put("/{tarefa_id}", response_model=TarefaOut)
# def editar(tarefa_id: int, tarefa_update: TarefaUpdate, db: Session = Depends(get_current_teacher)):
#     tarefa = tasks.editar_tarefa(db, tarefa_id, tarefa_update)
#     if not tarefa:
#         raise HTTPException(status_code=404, detail="Chamada não encontrada")
#     return tarefa

# @router.delete("/{tarefa_id}")
# def excluir(tarefa_id: int, db: Session = Depends(get_current_teacher)):
#     tarefa = tasks.excluir_tarefa(db, tarefa_id)
#     if not tarefa:
#         raise HTTPException(status_code=404, detail="Chamada não encontrada")
#     return {"message": "Chamada excluída com sucesso"}
