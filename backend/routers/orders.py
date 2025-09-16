from fastapi import APIRouter,Depends,HTTPException,status
import backend.models as models
import backend.schemas as schemas
import backend.utils as utils
from backend.database import get_db
import backend.oauth2 as oauth2
from sqlalchemy.orm import Session

router = APIRouter()



@router.post('/order')
def place_order(db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):
  cart_items = db.query(models.Cart).filter(models.Cart.user_id == current_user.username).all()

  if not cart_items:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cart is empty")
  
  
  total_price = 0
  order_items = []
  for cart_item in cart_items:
    total_price += cart_item.price
    order_items.append({
      "product_id":cart_item.product_id,
      "name": cart_item.product.name,
      "quantity": cart_item.quantity,
      "price": cart_item.price
    })

  order_details = {
        "items": order_items,
        "subtotal": total_price,
        "final_total": total_price   # (you can add discount, shipping later)
    }
  
  order = models.Order(
    user_id = current_user.username,
    total_price = total_price,
    order_details=order_details
  )

  db.add(order)

  db.query(models.Cart).filter(models.Cart.user_id == current_user.username).delete()

  db.commit()
  db.refresh(order)

  return order

@router.get('/order')
def get_orders(db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):
  orders = db.query(models.Order).filter(models.Order.user_id == current_user.username).all()

  return orders