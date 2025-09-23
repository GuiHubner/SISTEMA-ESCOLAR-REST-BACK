from pydantic import BaseModel
from typing import Optional

class TarefaBase(BaseModel):
    title: str
    description: Optional[str] = None
    peso: int
    data: str
    disciplina: str
    turma: str

class TarefaUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    peso: float | None = None
    data: str | None = None
    disciplina: str | None = None
    turma: str | None = None

class TarefaOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    email: str
    peso: int
    data: str
    disciplina: str
    turma: str

    class Config:
        from_attributes = True
