from pydantic import BaseModel   
from typing import Optional  


class UserCreateUpdatePydantic(BaseModel):
    username : str
    email : str

class UserViewPydantic(BaseModel):
    username : str
    email : str