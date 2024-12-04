from fastapi import APIRouter, status, HTTPException

from .database import get_engine
from .models import Atividade
from sqlmodel import Session, select

router = APIRouter()

@router.get("/atividades/")
def listar_atividades():
    session = Session(get_engine())
    statement = select(Atividade) 
    atividades = session.exec(statement).all()
    return atividades

"""



# Endpoints de Atividades
@router.post("/atividades/", status_code=201)
def criar_atividade(atividade: Atividade):
    with get_engine() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO atividades (titulo, descricao) VALUES (%s, %s) RETURNING id, titulo, descricao, tempo_acumulado, media_classificacao",
                (atividade.titulo, atividade.descricao)
            )
            atividade_criada = cursor.fetchone()
    return atividade_criada



@router.put("/atividades/{atividade_id}")
def atualizar_atividade(atividade_id: int, atividade: Atividade):
    with get_engine() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE atividades SET titulo = %s, descricao = %s WHERE id = %s RETURNING id, titulo, descricao, tempo_acumulado, media_classificacao",
                (atividade.titulo, atividade.descricao, atividade_id)
            )
            atividade_atualizada = cursor.fetchone()
    
    if not atividade_atualizada:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    return atividade_atualizada
    
"""