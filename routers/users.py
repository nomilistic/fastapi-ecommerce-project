from fastapi import APIRouter,Depends,HTTPException,status
import models
import schemas
import utils
from database import get_db
import oauth2
from sqlalchemy.orm import Session

router = APIRouter()

@router.put('/roles')
def make_admin(db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):
  
  userrole = db.query(models.UserRole).filter(models.UserRole.user_id == current_user.username).first()
  
  admin_role_id = db.query(models.Role.id).filter(models.Role.role == "admin").first()
  userrole.role_id = admin_role_id.id
  db.commit()

  return {f"User {current_user.username}'s role changed to admin"}



@router.post('/register',response_model=schemas.UserOut)
def register_user(user:schemas.UserRegister,db:Session=Depends(get_db)):

  hashed_password = utils.hash(user.password)
  user.password = hashed_password
  
  
  new_user = models.User(**user.dict())

  customer_role_id =  db.query(models.Role.id).filter(models.Role.role == "customer").first()
  new_userrole = models.UserRole(
    user_id = new_user.username,
    role_id = customer_role_id[0]
  )

  db.add(new_userrole)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user
