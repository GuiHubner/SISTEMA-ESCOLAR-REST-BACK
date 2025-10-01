from sqlalchemy.orm import Session
from src.models.teacher.notas import Nota
from src.schemas.teacher.notas import NotaBase
from src.core.security import get_current_user
from src.models.teacher.tasks import Tarefa
from src.models.user_model import User
from src.models.teacher.chamada import Chamada
import json

def listar_notas(db: Session, email: str):
    # lista notas apenas das turmas/disciplinas do professor
    return db.query(Nota).join(Tarefa).filter(Tarefa.email == email).all()


def criar_notas(db: Session, nota_in: NotaBase, email: str):
    # 1. Buscar tarefa correspondente
    tarefa = db.query(Tarefa).filter(
        Tarefa.title == nota_in.title,
        Tarefa.disciplina == nota_in.disciplina,
        Tarefa.turma == nota_in.turma,
        Tarefa.data == nota_in.data,
        Tarefa.peso == nota_in.peso,
        Tarefa.email == email
    ).first()

    if not tarefa:
        raise ValueError("Tarefa não encontrada.")

    # 2. Buscar chamada correspondente
    chamada = db.query(Chamada).filter(
        Chamada.disciplina == nota_in.disciplina,
        Chamada.turma == nota_in.turma,
        Chamada.email == email
    ).first()

    if not chamada:
        raise ValueError("Chamada não encontrada.")

    # 3. Garantir que vetores tenham o mesmo tamanho
    if len(nota_in.alunos) != len(nota_in.notas):
        raise ValueError("O número de alunos e de notas não corresponde.")

    # 4. Criar notas em lote
    notas_criadas = []
    for aluno_nome, nota_valor in zip(nota_in.alunos, nota_in.notas):
        aluno_existe = any(a.aluno_nome == aluno_nome for a in chamada.alunos)
        if not aluno_existe:
            continue  # ignora alunos que não estão na chamada

        nova_nota = Nota(
            tarefa_id=tarefa.id,
            chamada_id=chamada.id,
            aluno_nome=aluno_nome,
            nota_valor=nota_valor,
        )
        db.add(nova_nota)
        notas_criadas.append(nova_nota)

    db.commit()
    for n in notas_criadas:
        db.refresh(n)

    return notas_criadas



# def editar_chamada(db: Session, chamada_id: int, chamada_update: ChamadaUpdate, teacher: User):
#     chamada = db.query(Chamada).filter(
#         Chamada.id == chamada_id,
#         Chamada.email == teacher.email  # garante que só edita a própria chamada
#     ).first()

#     if not chamada:
#         return None

#     # zera a lista antiga e adiciona de novo
#     chamada.alunos.clear()
#     for aluno in chamada_update.alunos:
#         chamada.alunos.append(
#             ChamadaAluno(
#                 aluno_nome=aluno.aluno_nome,
#                 status_horas=aluno.status_horas,
#             )
#         )

#     chamada.data = chamada_update.data
#     chamada.disciplina = chamada_update.disciplina
#     chamada.turma = chamada_update.turma
#     chamada.horas_aula = chamada_update.horas_aula

#     db.commit()
#     db.refresh(chamada)
#     return chamada


# def excluir_chamada(db: Session, 
#                     chamada_id: int,
#                     teacher: User):
#     chamada = db.query(Chamada).filter(Chamada.id == chamada_id, Chamada.email == teacher.email).first()
#     if not chamada:
#         return None
#     db.delete(chamada)
#     db.commit()
#     return chamada
