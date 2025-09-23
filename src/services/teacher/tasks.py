from sqlalchemy.orm import Session
from src.models.teacher.tasks import Tarefa
from src.schemas.teacher.tasks import TarefaBase, TarefaUpdate

def listar_tarefas(db: Session, email: str):
    return db.query(Tarefa).filter(Tarefa.email == email).all()

def criar_tarefa(db: Session, tarefa: TarefaBase, email: str):
    nova_tarefa = Tarefa(
        title=tarefa.title,
        description=tarefa.description,
        email=email,
        peso=tarefa.peso,
        disciplina=tarefa.disciplina,
        data=tarefa.data,
        turma=tarefa.turma,
    )
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

def editar_tarefa(db: Session, tarefa_id: int, tarefa_update: TarefaUpdate):
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        return None

    if tarefa_update.title is not None:
        tarefa.title = tarefa_update.title
    if tarefa_update.description is not None:
        tarefa.description = tarefa_update.description
    if tarefa_update.peso is not None:
        tarefa.peso = tarefa_update.peso
    if tarefa_update.data is not None:
        tarefa.data = tarefa_update.data
    if tarefa_update.disciplina is not None:
        tarefa.disciplina = tarefa_update.disciplina
    if tarefa_update.turma is not None:
        tarefa.turma = tarefa_update.turma

    db.commit()
    db.refresh(tarefa)
    return tarefa

def excluir_tarefa(db: Session, tarefa_id: int):
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        return None
    db.delete(tarefa)
    db.commit()
    return tarefa
