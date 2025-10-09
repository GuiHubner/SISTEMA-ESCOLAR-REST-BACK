from src.models.user_model import User
from sqlalchemy.orm import Session
from src.schemas.alunos.infos import  InfosCombinedOut
from fastapi import APIRouter, Depends
from src.database import get_db
from src.services.alunos.infos import listar_infos
from src.core.security import get_current_aluno
from typing import Optional
from fastapi.encoders import jsonable_encoder
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/alunos/infos",
    tags=["Alunos - Info"]
)

@router.get("/", response_model=dict)
def listar_infos_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_aluno)
):
    dados = listar_infos(db, current_user.class_id, current_user.name)
    safe = jsonable_encoder(dados)
    logger.debug("listar_infos -> %s", safe)
    # Retorna o dict já serializável (não força InfosCombinedOut que espera outro formato)
    return safe