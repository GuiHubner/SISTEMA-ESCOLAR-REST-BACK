from pydantic import BaseModel
from typing import Optional, List

class InfosOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    email: str
    peso: int
    data: str
    disciplina: str
    turma: str

    class Config:
        orm_mode = True

class InfosCombinedOut(BaseModel):
    chamadas: List[InfosOut]
    notas: List[InfosOut]

    class Config:
        orm_mode = True
