from fastapi import APIRouter, status, HTTPException

from src.database import get_engine
from src.models import Registro
from sqlmodel import Session, select

router = APIRouter()
"""
# Endpoints de Registros
@router.post("/registros/{atividade_id}/", status_code=201)
def criar_registro(atividade_id: int, registro: Registro):
    
    return registro_criado

@router.put("/registros/{atividade_id}/{registro_id}/")
def editar_registro(atividade_id: int, registro_id: int, registro: Registro):
    
    return registro_atualizado

@router.get("/registros/")
def listar_registros(atividade_id: int):
    
    return registros

"""