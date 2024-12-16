from fastapi import FastAPI

import models
from data_base import engine
from routers import auth, predict, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(predict.router)
# app.include_router(admin.router)
app.include_router(users.router)



