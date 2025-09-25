from sqlalchemy.orm import Session
from src.models.teacher.chamada import Chamada, ChamadaAluno
from src.schemas.teacher.chamada import ChamadaBase
from src.core.security import get_current_user
from src.models.user_model import User
import json

def listar_chamadas(db: Session, email: str):
    # Aqui você pode filtrar se precisar, por ex:
    # chamadas apenas das turmas/disciplinas do professor
    return db.query(Chamada).filter(Chamada.email == email).all()

def criar_chamada(db: Session, chamada_in: ChamadaBase, email: str):
    chamada = Chamada(
        data=chamada_in.data,
        disciplina=chamada_in.disciplina,
        turma=chamada_in.turma,
        horas_aula=chamada_in.horas_aula,
        email=email,
    )

    for aluno in chamada_in.alunos:
        chamada.alunos.append(
            ChamadaAluno(
                aluno_nome=aluno.aluno_nome,
                status_horas=aluno.status_horas,  # já é uma lista, combina com JSON
            )
        )

    db.add(chamada)
    db.commit()
    db.refresh(chamada)
    return chamada

# def editar_tarefa(db: Session, tarefa_id: int, tarefa_update: TarefaUpdate):
#     tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
#     if not tarefa:
#         return None

#     if tarefa_update.title is not None:
#         tarefa.title = tarefa_update.title
#     if tarefa_update.description is not None:
#         tarefa.description = tarefa_update.description
#     if tarefa_update.peso is not None:
#         tarefa.peso = tarefa_update.peso
#     if tarefa_update.data is not None:
#         tarefa.data = tarefa_update.data
#     if tarefa_update.disciplina is not None:
#         tarefa.disciplina = tarefa_update.disciplina
#     if tarefa_update.turma is not None:
#         tarefa.turma = tarefa_update.turma

#     db.commit()
#     db.refresh(tarefa)
#     return tarefa

# def excluir_tarefa(db: Session, tarefa_id: int):
#     tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
#     if not tarefa:
#         return None
#     db.delete(tarefa)
#     db.commit()
#     return tarefa
