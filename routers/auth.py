from fastapi import APIRouter,Depends,HTTPException,status
import models
import schemas
import utils
from database import get_db
import oauth2
from sqlalchemy.orm import Session

router = APIRouter()



@router.post('/login',response_model=schemas.Token)
def login_user(user:schemas.UserLogin,db:Session=Depends(get_db)):

  user_from_db = db.query(models.User).filter(models.User.username == user.username).first()
  if not user_from_db:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Invalid Credentials")

  if not utils.verify(user.password,user_from_db.password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Invalid Credentials")

  access_token = oauth2.create_access_token(data={"username": user.username})
  return {"access_token": access_token, "token_type": "bearer"}
