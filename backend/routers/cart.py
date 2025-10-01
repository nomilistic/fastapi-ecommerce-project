from fastapi import APIRouter,Depends,HTTPException,status
import backend.models as models
import backend.schemas as schemas
import backend.utils as utils
from backend.database import get_db
import backend.oauth2 as oauth2
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/cart/add')
def add_to_cart(cart_item:schemas.AddToCart,db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):

  product=db.query(models.Product).filter(models.Product.name==cart_item.name).first()
  if not product:
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{cart_item.name}' not found"
        )

  if product.quantity_available < cart_item.quantity:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail = "Requested quantity exceeds available stock")
  
  new_cart_item=models.Cart(
        user_id=current_user.username,
        product_id=product.id,
        name = product.name,
        quantity=cart_item.quantity,
        price = product.price * cart_item.quantity
    )
  
  

  check_cart_query = db.query(models.Cart).filter(
    models.Cart.user_id == new_cart_item.user_id,
    models.Cart.product_id == new_cart_item.product_id)


  
  
  if check_cart_query.first():
    check_cart_query.first().quantity += new_cart_item.quantity
    db.commit()
  else:
    db.add(new_cart_item)
    
   
  product.quantity_available -= new_cart_item.quantity


  db.commit()

  return {f"{cart_item.quantity} x {cart_item.name} added to cart!"}


@router.get('/cart')
def get_cart(db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):
  cart_items = db.query(models.Cart).filter(models.Cart.user_id == current_user.username).all()

  return cart_items

@router.delete('/cart/{cart_id}')
def delete_from_cart(quantity:int,cart_id:int,db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):

  cart_item = db.query(models.Cart).filter(
        models.Cart.id == cart_id,
        models.Cart.user_id == current_user.username
    ).first()
  
  if not cart_item:
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cart item with id {cart_id} not found"
            )
  
  product = db.query(models.Product).filter(models.Product.id == cart_item.product_id).first()

  if cart_item.quantity - quantity >0:
    cart_item.quantity -= quantity
  elif cart_item.quantity - quantity == 0:
    db.delete(cart_item)
  else:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Quantity to delete exceeds quantity in cart")

  cart_item.price -= product.price*quantity

  product.quantity_available += cart_item.quantity

  db.commit()

  return {f"{quantity} x {product.name} removed from cart"}
