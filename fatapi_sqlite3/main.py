
# from db_models import User, get_db
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select


from fastapi import FastAPI, Depends
from user_router import user_router

app = FastAPI()

#perfix for base url
app.include_router(user_router, prefix="", tags=["User Router"]) 
