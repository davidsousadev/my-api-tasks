# Refatoração: Melhorar a qualidade interna de um código
# sem alterar o seu comportamento observável

# PEP-8: Manual de Estilo de Código de Python

from sqlalchemy import table
from sqlmodel import SQLModel, Field
from datetime import date, datetime
import datetime

# Modelos Pydantic

class PushAtividade(SQLModel):
    titulo: str = Field(min_length=1)
    descricao: str = Field(min_length=1)
    
class Atividade(PushAtividade, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tempo_acumulado: int | None = Field(default=0)
    media_classificacao: float | None = Field(default=0)
       

class PutRegistro(SQLModel):
    tempo: int = Field(..., ge=1) 
    classificacao: float = Field(..., ge=1, le=5)
    descricao: str = Field(..., min_length=1)

class PushRegistro(PutRegistro):    
    id_atividade: int = Field(..., foreign_key="atividade.id")
    

class Registro(PushRegistro, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: str = Field(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

class BaseUser(SQLModel):
  name: str
  email: str
  username: str
  

class User(BaseUser, table=True):
  id: int = Field(default=None, primary_key=True)
  password: str


class SignUpUserRequest(BaseUser):
  password: str
  confirm_password: str


class SignInUserRequest(SQLModel):
  username: str
  password: str