from sqlalchemy.orm import Session
from src.models.teacher.notas import Nota
from src.schemas.teacher.notas import NotaBase, AlunoNota, NotaUpdate
from src.core.security import get_current_user
from src.models.teacher.tasks import Tarefa
from src.models.user_model import User
from src.models.teacher.chamada import Chamada
import json
from typing import List, Dict, Any

def _group_notas(notas: List[Nota]) -> List[Dict]:
    groups: Dict[str, Dict] = {}
    for nota in notas:
        # chave de agrupamento: prefira tarefa_id quando existir, senão chamada_id
        key = f"t:{nota.tarefa_id}" if nota.tarefa_id else f"c:{nota.chamada_id}"
        if key not in groups:
            tarefa = getattr(nota, "tarefa", None)
            chamada = getattr(nota, "chamada", None)
            groups[key] = {
                "id": getattr(tarefa, "id", getattr(chamada, "id", None)) or getattr(nota, "id", None),
                "title": getattr(tarefa, "title", None) if tarefa else None,
                "disciplina": getattr(tarefa, "disciplina", None) if tarefa else None,
                "turma": getattr(tarefa, "turma", None) if tarefa else None,
                "data": getattr(tarefa, "data", None) if tarefa else getattr(chamada, "data", None),
                "peso": getattr(tarefa, "peso", None) if tarefa else None,
                "alunos": [],
            }
        groups[key]["alunos"].append({
            "aluno_nome": nota.aluno_nome,
            "nota_valor": nota.nota_valor
        })
    return list(groups.values())

def listar_notas(db: Session, email: str) -> List[Dict[str, Any]]:
    rows = db.query(Nota).join(Tarefa).filter(Tarefa.email == email).all()
    return _group_notas(rows)


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
    notas_criadas: List[Nota] = []
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

    # Retorna estrutura agrupada (um objeto por tarefa/chamada, com lista de alunos)
    return _group_notas(notas_criadas)


def editar_nota(db: Session, tarefa_id: int, nota_update: NotaUpdate, email: str):
    # busca a tarefa pelo id e pelo email do professor
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id, Tarefa.email == email).first()
    if not tarefa:
        return None

    # busca chamada correspondente para ligar as notas novas se necessário
    chamada = db.query(Chamada).filter(
        Chamada.disciplina == nota_update.disciplina,
        Chamada.turma == nota_update.turma,
        Chamada.email == email
    ).first()
    if not chamada:
        raise ValueError("Chamada não encontrada.")

    # atualiza os dados da tarefa
    tarefa.data = nota_update.data
    tarefa.disciplina = nota_update.disciplina
    tarefa.turma = nota_update.turma
    tarefa.peso = nota_update.peso

    # atualiza ou cria notas para cada aluno informado
    for aluno in nota_update.alunos:
        nota_row = db.query(Nota).filter(
            Nota.tarefa_id == tarefa.id,
            Nota.aluno_nome == aluno.aluno_nome
        ).first()
        if nota_row:
            nota_row.nota_valor = aluno.nota_valor
        else:
            nova = Nota(
                tarefa_id=tarefa.id,
                chamada_id=chamada.id,
                aluno_nome=aluno.aluno_nome,
                nota_valor=aluno.nota_valor
            )
            db.add(nova)

    db.commit()

    # busca todas as notas da tarefa e retorna o grupo (um único objeto)
    rows = db.query(Nota).filter(Nota.tarefa_id == tarefa.id).all()
    grupos = _group_notas(rows)
    return grupos[0] if grupos else None


def excluir_nota(db: Session, 
                    nota_id: int,
                    teacher: User):
    # tenta excluir por tarefa (grupo)
    tarefa = db.query(Tarefa).filter(Tarefa.id == nota_id, Tarefa.email == teacher.email).first()
    if tarefa:
        rows = db.query(Nota).filter(Nota.tarefa_id == tarefa.id).all()
        if not rows:
            return None
        for r in rows:
            db.delete(r)
        db.commit()
        return True

    # tenta excluir uma nota individual (verifica propriedade via tarefa ou chamada)
    nota = db.query(Nota).filter(Nota.id == nota_id).first()
    if not nota:
        return None

    # verifica dono pela tarefa relacionada
    if getattr(nota, "tarefa", None) and getattr(nota.tarefa, "email", None) == teacher.email:
        db.delete(nota)
        db.commit()
        return True

    # verifica dono pela chamada relacionada
    if getattr(nota, "chamada", None) and getattr(nota.chamada, "email", None) == teacher.email:
        db.delete(nota)
        db.commit()
        return True

    # sem permissão / não pertence ao professor
    return None
