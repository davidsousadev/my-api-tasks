from fastapi import FastAPI
from .tasks_controller import router as task_router
from .users_controller import router as user_router
from .database import init_db


app = FastAPI()

app.include_router(router=task_router,  
                    tags=["Tasks"])
app.include_router(router=user_router,  
                    tags=["Users"])

init_db()
