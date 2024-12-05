from fastapi import APIRouter, status, HTTPException, Response

from .database import get_engine
from .models import Atividade, PushAtividade
from sqlmodel import Session, select

router = APIRouter()

@router.get("", status_code=status.HTTP_200_OK)
def listar_atividades():
    session = Session(get_engine())
    statement = select(Atividade) 
    atividades = session.exec(statement).all()
    return atividades

@router.post('', status_code=status.HTTP_201_CREATED)
def criar_atividade(atividade: PushAtividade):
    nova_atividade = Atividade(
        titulo=atividade.titulo,
        descricao=atividade.descricao,
    )
    
    with Session(get_engine()) as session:
        session.add(nova_atividade)
        session.commit()
        session.refresh(nova_atividade)

    return nova_atividade

@router.put('/{atividade_id}')
def alterar_atividade(atividade_id: int, dados: PushAtividade):
  with Session(get_engine()) as session:
    sttm = select(Atividade).where(Atividade.id == atividade_id)
    atividade = session.exec(sttm).one_or_none()
    
    if atividade:
      atividade.titulo=dados.titulo
      atividade.descricao=dados.descricao
      session.add(atividade)
      session.commit()
      session.refresh(atividade)
      return atividade
  
  raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f'Atividade não localizado com id = {atividade_id}'
  )

@router.delete('/{atividade_id}')
def atividade_delete(atividade_id: int):
  session = Session(get_engine())

  sttm = select(Atividade).where(Atividade.id == atividade_id)
  atividade = session.exec(sttm).first()

  if not atividade:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='Atividade nao encontrada...')
  
  else:
    session.delete(atividade)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

