from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.schemas.teacher.tasks import TarefaBase, TarefaUpdate, TarefaOut
from src.core.security import get_current_user, get_current_teacher
from src.services.teacher import tasks
from src.models.user_model import User

router = APIRouter(
    prefix="/teacher/tasks",
    tags=["Professor - Tarefas"]
)

@router.get("/", response_model=List[TarefaOut])
def listar_tarefas(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    return tasks.listar_tarefas(db, current_user.email)

@router.post("/", response_model=TarefaOut)
def criar(
    tarefa: TarefaBase, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_teacher)):
    return tasks.criar_tarefa(db, tarefa, current_user.email)

@router.put("/{tarefa_id}", response_model=TarefaOut)
def editar(tarefa_id: int, 
           tarefa_update: TarefaUpdate, 
           db: Session = Depends(get_db),
           current_teacher: User = Depends(get_current_teacher)):
    tarefa = tasks.editar_tarefa(db, tarefa_id, tarefa_update, current_teacher)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@router.delete("/{tarefa_id}")
def excluir(tarefa_id: int, db: Session = Depends(get_current_teacher)):
    tarefa = tasks.excluir_tarefa(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa excluída com sucesso"}
