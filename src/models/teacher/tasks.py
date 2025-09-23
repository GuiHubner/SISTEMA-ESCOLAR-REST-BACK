from sqlalchemy import Column, Integer, String, Text
from src.database import Base

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    email = Column(String(100), nullable=False)
    peso = Column(Integer, nullable=False)
    data = Column(String(100), nullable=False)
    disciplina = Column(String(100), nullable=False)
    turma = Column(String(100), nullable=True)