from fastapi import APIRouter,Depends,HTTPException,status
import models
import schemas
import utils
from database import get_db
import oauth2
from sqlalchemy.orm import Session
import permissions

router = APIRouter()




@router.post('/roles')
def add_role(role:schemas.Role,db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user), _: None = Depends(permissions.admin_required)):
  
  new_role = models.Role(**role.dict())
  db.add(new_role)
  db.commit()
  db.refresh(new_role)
  return new_role

@router.delete('/roles/{id}')
def delete_role(id:int,db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user), _: None = Depends(permissions.admin_required)):
  db.query(models.Role).filter(models.Role.id == id).delete()
  return {"Role Deleted!"}
