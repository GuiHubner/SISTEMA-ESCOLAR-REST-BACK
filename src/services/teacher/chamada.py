from sqlalchemy.orm import Session
from src.models.teacher.chamada import Chamada, ChamadaAluno
from src.schemas.teacher.chamada import ChamadaBase, ChamadaUpdate
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

def editar_chamada(db: Session, chamada_id: int, chamada_update: ChamadaUpdate, teacher: User):
    chamada = db.query(Chamada).filter(
        Chamada.id == chamada_id,
        Chamada.email == teacher.email  # garante que só edita a própria chamada
    ).first()

    if not chamada:
        return None

    # zera a lista antiga e adiciona de novo
    chamada.alunos.clear()
    for aluno in chamada_update.alunos:
        chamada.alunos.append(
            ChamadaAluno(
                aluno_nome=aluno.aluno_nome,
                status_horas=aluno.status_horas,
            )
        )

    chamada.data = chamada_update.data
    chamada.disciplina = chamada_update.disciplina
    chamada.turma = chamada_update.turma
    chamada.horas_aula = chamada_update.horas_aula

    db.commit()
    db.refresh(chamada)
    return chamada


def excluir_chamada(db: Session, 
                    chamada_id: int,
                    teacher: User):
    chamada = db.query(Chamada).filter(Chamada.id == chamada_id, Chamada.email == teacher.email).first()
    if not chamada:
        return None
    db.delete(chamada)
    db.commit()
    return chamada
