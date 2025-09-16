from fastapi import APIRouter,Depends,HTTPException,status
import models
import schemas
import utils
from database import get_db
import oauth2
from sqlalchemy.orm import Session
import permissions

router = APIRouter()


@router.post('/products')
def add_product(product:schemas.Product,db:Session = Depends(get_db),current_user:str = Depends(oauth2.get_current_user), _: None = Depends(permissions.admin_required)):
  new_product = models.Product(**product.dict())

  db.add(new_product)
  db.commit()
  db.refresh(new_product)
  return new_product

@router.put('/products/{product_id}')
def update_product(product:schemas.Product,product_id:int,db:Session = Depends(get_db),current_user:str = Depends(oauth2.get_current_user), _: None = Depends(permissions.admin_required)):
  product_to_update = db.query(models.Product).filter(models.Product.id == product_id).first()

  if not product_to_update:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id {product_id} not found")
  
  product_to_update.name = product.name
  product_to_update.price = product.price
  product_to_update.quantity_available= product.quantity_available
  
  

  db.commit()
  db.refresh(product_to_update)
  return product_to_update 


@router.delete('/products/{id}')
def delete_product(id:int,db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user), _: None = Depends(permissions.admin_required)):
  
  product_query = db.query(models.Product).filter(models.Product.id == id)

  if not product_query.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id {id} not found")
  
  product_query.delete(synchronize_session=False)

  db.commit()

  return {'message':'product was successfully deleted'}


@router.get('/products')
def get_products(db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):

  return db.query(models.Product).all()

@router.get('/products/{id}')
def get_product_by_id(id:int,db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):

  product = db.query(models.Product).filter(models.Product.id==id).first()

  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product with id {id} not found")
  
  return product

