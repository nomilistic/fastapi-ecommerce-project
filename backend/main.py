from fastapi import FastAPI
# import models
# from database import engine
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth,users,roles,products,cart,orders

# not needed after alembic now
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:8501","https://www.google.com"]
app.add_middleware(
  CORSMiddleware,
  allow_origins = origins,
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ["*"]
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)

@app.get('/')
def open_app():
  return {"hello! welcome to enomi"}


