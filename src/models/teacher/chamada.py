from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, validates
from src.database import Base
from sqlalchemy import JSON


class Chamada(Base):
    __tablename__ = "chamada"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False)
    disciplina = Column(String, nullable=False)
    turma = Column(String, nullable=False)
    horas_aula = Column(Integer, nullable=False)
    email = Column(String(100), nullable=False)
    finalized = Column(Integer, default=0)
    ano = Column(Integer, nullable=False)

    # relacionamento com chamada_aluno
    alunos = relationship("ChamadaAluno", back_populates="chamada", cascade="all, delete")

    notas = relationship("Nota", back_populates="chamada") ####### apagar se der erro


    @validates("data")
    def set_ano(self, key, value):
        if value:
            self.ano = value.year
        return value


class ChamadaAluno(Base):
    __tablename__ = "chamada_aluno"

    id = Column(Integer, primary_key=True, index=True)
    chamada_id = Column(Integer, ForeignKey("chamada.id", ondelete="CASCADE"))
    aluno_nome = Column(String, nullable=False)
    status_horas = Column(JSON, nullable=False)

    chamada = relationship("Chamada", back_populates="alunos")
