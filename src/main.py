from fastapi import FastAPI
from sqlmodel import SQLModel
from .atividades_controller import router as atividades_router
from .registros_controller import router as registros_router
from .database import get_engine
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from decouple import config
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional

app = FastAPI()

# Configuração de CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(atividades_router, 
                   prefix='/atividades')
app.include_router(registros_router, 
                   prefix='/registros')

# Criar DB
SQLModel.metadata.create_all(get_engine())

# URL do banco de dados
DATABASE_URL = config('DATABASE_URL')




# Função auxiliar para atualizar métricas da atividade
def atualizar_metricas_atividade(atividade_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(tempo), 0) AS tempo_acumulado,
                    COALESCE(AVG(classificacao), 0) AS media_classificacao
                FROM registros
                WHERE atividade_id = %s
            """, (atividade_id,))
            resultado = cursor.fetchone()
            tempo_acumulado, media_classificacao = resultado["tempo_acumulado"], resultado["media_classificacao"]

            cursor.execute("""
                UPDATE atividades
                SET tempo_acumulado = %s, media_classificacao = %s
                WHERE id = %s
            """, (tempo_acumulado, media_classificacao, atividade_id))
            conn.commit()

# Criação das tabelas
def criar_tabelas():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS atividades (
                        id SERIAL PRIMARY KEY,
                        titulo VARCHAR NOT NULL,
                        descricao VARCHAR,
                        tempo_acumulado INTEGER DEFAULT 0,
                        media_classificacao FLOAT DEFAULT 0.0
                    );
                    CREATE TABLE IF NOT EXISTS registros (
                        id SERIAL PRIMARY KEY,
                        atividade_id INTEGER REFERENCES atividades(id) ON DELETE CASCADE,
                        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        tempo INTEGER NOT NULL,
                        classificacao INTEGER NOT NULL,
                        descricao VARCHAR NOT NULL
                    );
                """)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise HTTPException(status_code=500, detail=f"Erro ao criar tabelas: {e}")

# Inicializa as tabelas
criar_tabelas()

# Endpoints de Atividades
@app.post("/atividades/", status_code=201)
def criar_atividade(atividade: Atividade):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO atividades (titulo, descricao) VALUES (%s, %s) RETURNING id, titulo, descricao, tempo_acumulado, media_classificacao",
                (atividade.titulo, atividade.descricao)
            )
            atividade_criada = cursor.fetchone()
    return atividade_criada

@app.get("/atividades/")
def listar_atividades():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM atividades")
            atividades = cursor.fetchall()
    return atividades

@app.put("/atividades/{atividade_id}")
def atualizar_atividade(atividade_id: int, atividade: Atividade):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE atividades SET titulo = %s, descricao = %s WHERE id = %s RETURNING id, titulo, descricao, tempo_acumulado, media_classificacao",
                (atividade.titulo, atividade.descricao, atividade_id)
            )
            atividade_atualizada = cursor.fetchone()
    
    if not atividade_atualizada:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    return atividade_atualizada

# Endpoints de Registros
@app.post("/registros/{atividade_id}/", status_code=201)
def criar_registro(atividade_id: int, registro: Registro):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO registros (atividade_id, tempo, classificacao, descricao)
                VALUES (%s, %s, %s, %s)
                RETURNING id, atividade_id, tempo, classificacao, descricao, data
            """, (atividade_id, registro.tempo, registro.classificacao, registro.descricao))
            registro_criado = cursor.fetchone()
            conn.commit()
    
    atualizar_metricas_atividade(atividade_id)
    return registro_criado

@app.put("/registros/{atividade_id}/{registro_id}/")
def editar_registro(atividade_id: int, registro_id: int, registro: Registro):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE registros
                SET tempo = %s, classificacao = %s, descricao = %s
                WHERE id = %s AND atividade_id = %s
                RETURNING id, atividade_id, tempo, classificacao, descricao, data
            """, (registro.tempo, registro.classificacao, registro.descricao, registro_id, atividade_id))
            registro_atualizado = cursor.fetchone()
    
    if not registro_atualizado:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    atualizar_metricas_atividade(atividade_id)
    return registro_atualizado

@app.get("/registros/")
def listar_registros(atividade_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, tempo, classificacao, descricao, data FROM registros WHERE atividade_id = %s", (atividade_id,))
            registros = cursor.fetchall()
    
    if not registros:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado para a atividade especificada")
    
    return registros
