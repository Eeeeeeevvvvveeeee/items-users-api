from fastapi import FastAPI
import src.models as models
from src.database import engine
from src.routes import items,users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="2 API User and Item -Using Postman")

@app.get("/")
def home():
    return {"message": "API is working"}
#items
app.include_router(items.router)
#Users
app.include_router(users.router)
