from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, File, UploadFile
from starlette import status
from inference import read_license_plate
from models import Predict
from data_base import SessionLocal
from .auth import get_current_user
import numpy as np

router = APIRouter(
    prefix='/prediction',
    tags=['prediction'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class PredictRequest(BaseModel):
    image_path: str

@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Predict).filter(Predict.owner_id == user.get('id')).all()

@router.get("/{prediction_id}", status_code=status.HTTP_200_OK)
async def read_prediction(user: user_dependency, db: db_dependency, prediction_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    prediction_model = db.query(Predict).filter(Predict.id == prediction_id).filter(Predict.owner_id == user.get('id')).first()
    if prediction_model is not None:
        return prediction_model
    raise HTTPException(status_code=404, detail='Prediction not found')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def make_prediction(user: user_dependency, db: db_dependency, predict_request: UploadFile):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    print('############################################')
    print(f'type image {predict_request}')
    
    # Read the file contents
    image = await predict_request.read()
    # Convert the file bytes to a NumPy array
    file_array = np.frombuffer(image, np.uint8)

    result = read_license_plate(file_array)
    # result = 2
    prediction_model = Predict(
        image_path=predict_request.filename,
        model='YOLOv11 + OCR',
        #score=0.0,  # If you have a specific score, update it here.
        result=result,  # Assuming result is the class predicted.
        owner_id=user.get('id')
    )
    db.add(prediction_model)
    db.commit()
    return prediction_model

@router.delete("/{prediction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prediction(user: user_dependency, db: db_dependency, prediction_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    prediction_model = db.query(Predict).filter(Predict.id == prediction_id).filter(Predict.owner_id == user.get('id')).first()
    if prediction_model is None:
        raise HTTPException(status_code=404, detail='Prediction not found')
    db.query(Predict).filter(Predict.id == prediction_id).filter(Predict.owner_id == user.get('id')).delete()
    db.commit()
