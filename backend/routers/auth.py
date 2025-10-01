from fastapi import APIRouter,Depends,HTTPException,status
import backend.models as models
import backend.schemas as schemas
import backend.utils as utils
from backend.database import get_db
import backend.oauth2 as oauth2
from sqlalchemy.orm import Session

router = APIRouter()



@router.post('/login')
def login_user(user:schemas.UserLogin,db:Session=Depends(get_db)):

  user_from_db = db.query(models.User).filter(models.User.username == user.username).first()
  if not user_from_db:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Invalid Credentials")

  if not utils.verify(user.password,user_from_db.password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Invalid Credentials")


  user_role_id = db.query(models.UserRole.role_id).filter(models.UserRole.user_id == user.username).first()
  
  user_role = db.query(models.Role.role).filter(models.Role.id == user_role_id[0]).first()
  
  access_token = oauth2.create_access_token(data={"username": user.username})
  return {"access_token": access_token, "token_type": "bearer","role":user_role[0]}
