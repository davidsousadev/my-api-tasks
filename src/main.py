from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from .atividades_controller import router as atividades_router
from .registros_controller import router as registros_router
from .database import get_engine

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(atividades_router, prefix='/atividades', tags=["Atividades"])
app.include_router(registros_router, prefix='/registros', tags=["Registros"])

# Criar DB
SQLModel.metadata.create_all(get_engine())

from fastapi.middleware.trustedhost import TrustedHostMiddleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])  