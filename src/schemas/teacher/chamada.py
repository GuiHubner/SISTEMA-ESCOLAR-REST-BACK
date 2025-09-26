from pydantic import BaseModel, Field, validator
from typing import List
from datetime import date

class AlunoChamada(BaseModel):
    aluno_nome: str
    status_horas: List[str]  # ["P", "F", "P"]

class ChamadaBase(BaseModel):
    data: date
    disciplina: str
    turma: str
    horas_aula: int = Field(..., gt=0, le=5)  # exemplo: 1 até 5 períodos
    alunos: List[AlunoChamada]

    @validator("alunos", each_item=True)
    def validar_status_por_hora(cls, aluno, values):
        horas_aula = values.get("horas_aula")
        if horas_aula and len(aluno.status_horas) != horas_aula:
            raise ValueError(
                f"O aluno {aluno.aluno_nome} precisa ter {horas_aula} registros em status_horas"
            )
        return aluno

class ChamadaUpdate(BaseModel):
    data: date
    disciplina: str
    turma: str
    horas_aula: int = Field(..., gt=0, le=5)  # exemplo: 1 até 5 períodos
    alunos: List[AlunoChamada]

    @validator("alunos", each_item=True)
    def validar_status_por_hora(cls, aluno, values):
        horas_aula = values.get("horas_aula")
        if horas_aula and len(aluno.status_horas) != horas_aula:
            raise ValueError(
                f"O aluno {aluno.aluno_nome} precisa ter {horas_aula} registros em status_horas"
            )
        return aluno

class ChamadaOut(ChamadaBase):
    id: int
    ano: int
    email: str
    alunos: List[AlunoChamada] 

    @validator("alunos", each_item=True)
    def validar_status_por_hora(cls, aluno, values):
        horas_aula = values.get("horas_aula")
        if horas_aula and len(aluno.status_horas) != horas_aula:
            raise ValueError(
                f"O aluno {aluno.aluno_nome} precisa ter {horas_aula} registros em status_horas"
            )
        return aluno

    class Config:
        from_attributes = True
