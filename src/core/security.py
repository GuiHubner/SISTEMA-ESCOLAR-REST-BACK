from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.user_model import User

# Configurações JWT
SECRET_KEY = "sua_chave_super_secreta"  # troque em produção!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Funções de senha
def verificar_senha(senha_plana: str, senha_hash: str):
    return pwd_context.verify(senha_plana, senha_hash)

def gerar_hash_senha(senha: str):
    return pwd_context.hash(senha)

# Funções JWT
def criar_token(dados: dict, expires_delta: Optional[timedelta] = None):
    to_encode = dados.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decodificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Função para obter o usuário atual
async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user

# Função para verificar se o usuário é professor
async def get_current_teacher(current_user: User = Depends(get_current_user)) -> User:
    if current_user.level != "professor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não tem permissões de professor"
        )
    return current_user

async def get_current_aluno(current_user: User = Depends(get_current_user)) -> User:
    if current_user.level != "aluno":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não tem permissões de aluno"
        )
    return current_user

async def get_current_coordenacao(current_user: User = Depends(get_current_user)) -> User:
    if current_user.level != "coordenacao":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não tem permissões de coordenacao"
        )
    return current_user

async def get_teacher_or_coordenacao(current_user: User = Depends(get_current_user)) -> User:
    if current_user.level not in ("teacher", "coordenacao"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas professores ou coordenação podem acessar esta rota"
        )
    return current_user

async def get_users_for_prof_or_coord(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[User]:
    if current_user.level == "coordenacao":
        # Coordenação vê todos
        return db.query(User).all()
    elif current_user.level == "teacher":
        # Professor vê apenas ele mesmo
        return [current_user]
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas professores ou coordenação podem acessar esta rota"
        )