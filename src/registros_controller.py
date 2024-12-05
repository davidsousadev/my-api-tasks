from fastapi import APIRouter, status, HTTPException
from src.database import get_engine
from src.models import Registro, PutRegistro, PushRegistro, Atividade
from sqlmodel import Session, select

router = APIRouter()

@router.get('/{id_atividade}', status_code=200)
def listar_registros_por_atividade(id_atividade: int):
    with Session(get_engine()) as session:
        registros = session.exec(
            select(Registro).where(Registro.id_atividade == id_atividade)
        ).all()
        
        if not registros:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado para a atividade especificada")
        
        return registros

@router.post('', status_code=201)
def criar_registro(registro: PushRegistro):
    with Session(get_engine()) as session:
        
        atividade = session.exec(select(Atividade).where(Atividade.id == registro.id_atividade)).first()
        if not atividade:
            raise HTTPException(status_code=404, detail="Atividade não encontrada")
        
        novo_registro = Registro(
            tempo=registro.tempo,
            classificacao=registro.classificacao,
            descricao=registro.descricao,
            id_atividade=registro.id_atividade
        )
        session.add(novo_registro)
        session.commit()
        session.refresh(novo_registro)
        
        atividade.tempo_acumulado += registro.tempo
        registros_atividade = session.exec(
            select(Registro.classificacao).where(Registro.id_atividade == registro.id_atividade)
        ).all()
        atividade.media_classificacao = round(sum(registros_atividade) / len(registros_atividade), 2)

        session.add(atividade)
        session.commit()
        session.refresh(atividade)

        return novo_registro

@router.put('/{registro_id}', status_code=200)
def atualizar_registro(registro_id: int, registro: PutRegistro):
    with Session(get_engine()) as session:
        registro_existente = session.exec(select(Registro).where(Registro.id == registro_id)).first()
        if not registro_existente:
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        
        registro_existente.tempo = registro.tempo
        registro_existente.classificacao = registro.classificacao
        registro_existente.descricao = registro.descricao
        session.add(registro_existente)
        session.commit()
        session.refresh(registro_existente)

        atividade = session.exec(select(Atividade).where(Atividade.id == registro_existente.id_atividade)).first()
        if not atividade:
            raise HTTPException(status_code=404, detail="Atividade não encontrada")
        
        registros_atividade = session.exec(select(Registro).where(Registro.id_atividade == atividade.id)).all()
        atividade.tempo_acumulado = sum(r.tempo for r in registros_atividade)
        atividade.media_classificacao = round(
            sum(r.classificacao for r in registros_atividade) / len(registros_atividade), 2
        )

        session.add(atividade)
        session.commit()
        session.refresh(atividade)

        return registro_existente

@router.delete('/{registro_id}', status_code=204)
def deletar_registro(registro_id: int):
    with Session(get_engine()) as session:
        registro = session.exec(select(Registro).where(Registro.id == registro_id)).first()
        if not registro:
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        
        atividade = session.exec(select(Atividade).where(Atividade.id == registro.id_atividade)).first()
        if not atividade:
            raise HTTPException(status_code=404, detail="Atividade não encontrada")

        session.delete(registro)
        session.commit()

        registros_atividade = session.exec(select(Registro).where(Registro.id_atividade == atividade.id)).all()
        atividade.tempo_acumulado = sum(r.tempo for r in registros_atividade)

        if registros_atividade:
            atividade.media_classificacao = sum(r.classificacao for r in registros_atividade) / len(registros_atividade)
        else:
            atividade.media_classificacao = 0  
        session.add(atividade)
        session.commit()
        session.refresh(atividade)

        return {"message": "Registro excluído e atividade atualizada com sucesso"}