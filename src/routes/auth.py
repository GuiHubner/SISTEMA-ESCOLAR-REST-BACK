from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from src.core.enums import UserType
import datetime
import random
from typing import List

# Get the current year
current_year = datetime.datetime.now().year

# Generate a random integer between a specified range (e.g., 1 and 100)
random_number = random.randint(1, 100)

print(f"Current year: {current_year}")
print(f"Random number: {random_number}")

from src.database import get_db
from src.models.user_model import User
from src.schemas.user import UserCreate, UserOut
from src.core.security import verificar_senha, gerar_hash_senha, criar_token, decodificar_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.get("/cadastrados", response_model=List[UserOut])
def listar_registros(db: Session = Depends(get_db)):
    return db.query(User).all()

# ---------------- CADASTRAR USUÁRIO ----------------
@router.post("/register", response_model=UserOut)
def registrar(user: UserCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(User).filter(User.email == user.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já registrado")

    senha_hash = gerar_hash_senha(user.password)
    
    novo_user = User(
        name=user.name,
        email=user.email,
        password=senha_hash,
        level=user.level,
        school=user.school,
        tel=user.tel,
        address=user.address,

        class_id=user.class_id,
        registration_number=user.registration_number,

        parent_name=user.parent_name,
        parent_tel=user.parent_tel,
        parent_email=user.parent_email
    )

    # Additional fields for student
    if user.level == UserType.STUDENT:
        if not user.class_id:
            raise HTTPException(status_code=400, detail="Turma é obrigatória para estudantes")
        novo_user.class_id = user.class_id
        novo_user.registration_number = f"STD{datetime.now().year}{random.randint(1000, 9999)}"

    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    return novo_user


# ---------------- LOGIN ----------------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.email == form_data.username).first()
    if not usuario or not verificar_senha(form_data.password, usuario.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = criar_token(
        dados={"sub": usuario.email, "tipo": usuario.level},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------- PEGAR USUÁRIO ATUAL ----------------
@router.get("/me", response_model=UserOut)
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decodificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    email: str = payload.get("sub")
    usuario = db.query(User).filter(User.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario
