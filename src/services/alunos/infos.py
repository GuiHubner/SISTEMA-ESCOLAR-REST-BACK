from sqlalchemy.orm import Session, joinedload
from src.models.teacher.chamada import Chamada, ChamadaAluno
from src.models.teacher.notas import Nota
from src.models.teacher.tasks import Tarefa
from typing import Optional, Dict, Any, List
import pandas as pd

def listar_infos(db: Session, class_id: str, name: str) -> Dict[str, List[Any]]:
    """
    Retorna chamadas e notas do aluno (por email) e opcionalmente filtradas por turma.
    """
    notas = (
        db.query(Nota)
        .join(Tarefa, Nota.tarefa_id == Tarefa.id)
        .filter(
            Nota.aluno_nome == name,
            Tarefa.turma == class_id
        )
        .options(joinedload(Nota.tarefa))
        .all()
    )

    notas_resultado = []
    for nota in notas:
        notas_resultado.append({
            # "aluno_nome": nota.aluno_nome,
            "nota_valor": nota.nota_valor,
            # "created_at": nota.created_at,
            "tarefa": {
                # "id": nota.tarefa.id,
                "title": nota.tarefa.title,
                "description": nota.tarefa.description,
                # "email": nota.tarefa.email,
                "peso": nota.tarefa.peso,
                "data": nota.tarefa.data,
                "disciplina": nota.tarefa.disciplina,
                # "turma": nota.tarefa.turma,
            }
        })

    chamadas = (
        db.query(Chamada)
        .join(ChamadaAluno, Chamada.id == ChamadaAluno.chamada_id)
        .filter(
            Chamada.turma == class_id,
            ChamadaAluno.aluno_nome == name
        )
        .options(joinedload(Chamada.alunos))
        .all()
    )

    chamadas_resultado = []
    for chamada in chamadas:
        # Filtra apenas o registro do aluno atual
        aluno = next(
            (a for a in chamada.alunos if a.aluno_nome == name),
            None
        )
        chamadas_resultado.append({
            # "id": chamada.id,
            "data": str(chamada.data),
            "disciplina": chamada.disciplina,
            # "turma": chamada.turma,
            "horas_aula": chamada.horas_aula,
            # "email": chamada.email,
            "ano": chamada.ano,
            # "finalized": chamada.finalized,
            "aluno": {
                # "aluno_nome": aluno.aluno_nome if aluno else None,
                "status_horas": aluno.status_horas if aluno else None,
            }
        })

    # === RESULTADO FINAL ===
    return {
        "aluno": name,
        "turma": class_id,
        "notas": notas_resultado,
        "chamadas": chamadas_resultado
    }