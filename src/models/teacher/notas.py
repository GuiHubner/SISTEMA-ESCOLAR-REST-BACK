from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, validates
from src.database import Base
from sqlalchemy import JSON
import datetime

class Nota(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, index=True)
    tarefa_id = Column(Integer, ForeignKey("tarefas.id"))
    chamada_id = Column(Integer, ForeignKey("chamada.id"))
    aluno_nome = Column(String)  # vem de ChamadaAluno

    nota_valor = Column(Float)
    created_at = Column(String)

    # Relações
    tarefa = relationship("Tarefa", back_populates="notas")
    chamada = relationship("Chamada", back_populates="notas")
