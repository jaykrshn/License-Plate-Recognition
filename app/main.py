from fastapi import FastAPI
from .models import Base
from .data_base import engine
from .routers import auth, predict, users, admin

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(admin.router)
app.include_router(users.router)