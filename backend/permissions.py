from fastapi import Depends,HTTPException,status
import backend.models as models
import backend.schemas as schemas
import backend.utils as utils
from backend.database import get_db
import backend.oauth2 as oauth2
from sqlalchemy.orm import Session


def admin_required(current_user = Depends(oauth2.get_current_user),db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.username == current_user.username).first()
  
  userrole = db.query(models.UserRole).filter(models.UserRole.user_id == user.username).first()
  
  role = db.query(models.Role).filter(models.Role.id == userrole.role_id).first()
  if role.role != "admin":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

  return True 
