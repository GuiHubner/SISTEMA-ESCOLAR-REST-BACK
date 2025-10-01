from pydantic import BaseModel, Field, validator, root_validator
from typing import List
from datetime import date
from typing import Optional, Any

class NotaBase(BaseModel):
    title: str
    disciplina: str
    turma: str
    data: str
    peso: float
    alunos: List[str]
    notas: List[float]

class NotaOut(BaseModel):
    id: int
    title: Optional[str]
    disciplina: Optional[str]
    turma: Optional[str]
    data: Optional[str]
    peso: Optional[float]
    aluno_nome: Optional[str]
    nota_valor: Optional[float]

    @root_validator(pre=True)
    def populate_from_relations(cls, values: Any):
        # values pode ser um dict (já serializado) ou a instância ORM
        if not isinstance(values, dict):
            obj = values
            tarefa = getattr(obj, "tarefa", None)
            chamada = getattr(obj, "chamada", None)
            return {
                "id": getattr(obj, "id", None),
                "title": getattr(tarefa, "title", None) if tarefa else None,
                "disciplina": getattr(tarefa, "disciplina", None) if tarefa else None,
                "turma": getattr(tarefa, "turma", None) if tarefa else None,
                "data": getattr(tarefa, "data", None) if tarefa else getattr(chamada, "data", None),
                "peso": getattr(tarefa, "peso", None) if tarefa else None,
                "aluno_nome": getattr(obj, "aluno_nome", None),
                "nota_valor": getattr(obj, "nota_valor", None),
            }
        return values

    class Config:
        orm_mode = True



# class ChamadaUpdate(BaseModel):
#     data: date
#     disciplina: str
#     turma: str
#     horas_aula: int = Field(..., gt=0, le=5)  # exemplo: 1 até 5 períodos
#     alunos: List[AlunoChamada]

#     @validator("alunos", each_item=True)
#     def validar_status_por_hora(cls, aluno, values):
#         horas_aula = values.get("horas_aula")
#         if horas_aula and len(aluno.status_horas) != horas_aula:
#             raise ValueError(
#                 f"O aluno {aluno.aluno_nome} precisa ter {horas_aula} registros em status_horas"
#             )
#         return aluno

# class NotasOut(NotaBase):
#     id: int
#     ano: int
#     email: str
#     alunos: List[AlunoNotas] 

#     @validator("alunos", each_item=True)
#     def validar_status_por_hora(cls, aluno, values):
#         horas_aula = values.get("horas_aula")
#         if horas_aula and len(aluno.status_horas) != horas_aula:
#             raise ValueError(
#                 f"O aluno {aluno.aluno_nome} precisa ter {horas_aula} registros em status_horas"
#             )
#         return aluno

#     class Config:
#         from_attributes = True
