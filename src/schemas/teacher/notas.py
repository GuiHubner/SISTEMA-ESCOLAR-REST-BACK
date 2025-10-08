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

class AlunoNota(BaseModel):
    aluno_nome: str
    nota_valor: float

class NotasGroupOut(BaseModel):
    id: int
    title: Optional[str]
    disciplina: Optional[str]
    turma: Optional[str]
    data: Optional[str]
    peso: Optional[float]
    alunos: List[AlunoNota]

    class Config:
        orm_mode = True

class NotaUpdate(BaseModel):
    data: date
    disciplina: str
    turma: str
    peso: float # exemplo: 1 até 5 períodos
    alunos: List[AlunoNota]

    @validator("alunos", each_item=True)
    def validar_status_por_hora(cls, aluno, values):
        horas_aula = values.get("horas_aula")
        if horas_aula and len(aluno.status_horas) != horas_aula:
            raise ValueError(
                f"O aluno {aluno.aluno_nome} precisa ter {horas_aula} registros em status_horas"
            )
        return aluno