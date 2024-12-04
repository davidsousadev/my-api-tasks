# Refatoração: Melhorar a qualidade interna de um código
# sem alterar o seu comportamento observável

# PEP-8: Manual de Estilo de Código de Python

from sqlalchemy import table
from sqlmodel import SQLModel, Field

# Modelos Pydantic
class Atividade(BaseModel):
    titulo: str
    descricao: Optional[str] = None

class Registro(BaseModel):
    tempo: int
    classificacao: int
    descricao: str