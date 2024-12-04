# Refatoração: Melhorar a qualidade interna de um código
# sem alterar o seu comportamento observável

# PEP-8: Manual de Estilo de Código de Python

from sqlalchemy import table
from sqlmodel import SQLModel, Field

# Modelos Pydantic
class Atividade(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str = Field(min_length=1)
    descricao: str = Field(min_length=1)

class Registro(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tempo: int = Field(min_length=1)
    classificacao: int = Field(max_length=1)
    descricao: str = Field(min_length=1)