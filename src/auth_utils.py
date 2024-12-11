from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import Session, select
from decouple import config
from src.database import get_engine
from src.models import User

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='signin')

async def get_logged_user(token: Annotated[str, Depends(oauth2_scheme)]):
  # Vai pegar o Token na Request, se válido
  # pegará o usuário no BD para confirmar e retornar ele
  exception = HTTPException(status_code=401, detail='Não autorizado!')

  payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
  username = payload.get('sub')

  if not username: 
    raise exception
  
  with Session(get_engine()) as session:
    sttm = select(User).where(User.username == username)
    user = session.exec(sttm).first()

    if not user:
      raise exception
    
    return user