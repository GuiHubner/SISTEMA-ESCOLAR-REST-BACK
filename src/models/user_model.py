from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from src.database import Base
from src.core.enums import UserType

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Nome do aluno
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(200), nullable=False)  # Senha hasheada
    level = Column(String(20), nullable=False)  # "aluno", "professor", "admin"
    school = Column(String(200), nullable=False)

    # Contatos
    tel = Column(String(20), nullable=True)  # Telefone do aluno
    address = Column(String(200), nullable=True)

    # Dados acadêmicos
    class_id = Column(Integer, nullable=True)  # Turma
    registration_number = Column(String, nullable=True, unique=True)

    # Dados do responsável
    parent_name = Column(String(100), nullable=True)
    parent_tel = Column(String(20), nullable=True)
    parent_email = Column(String(100), nullable=True)