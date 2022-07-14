import random
from typing import List
import numpy as np
from fastapi import Depends, FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
app = FastAPI()

oauth_scheme = OAuth2PasswordBearer(tokenUrl= "token")

@app.post("/token")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    return {"access token":form_data.username , "token_type": 'bearer'}

@app.get("/login")
async def login(token: str = Depends(oauth_scheme)):
    print(token)
    return {
        "user" : "user123",
        "password" : "1234"
    }



class User(BaseModel):
    user_id : str = input('Please Enter A Name: ')
    user_age : int = int(input('Please Enter An Age: '))
    user_score : list[float] =[random.random()* 10, random.random()* 10, random.random()* 10, random.random()* 10, random.random()* 10 ] 

@app.get("/")
def root():
    return {"Hello", "Mundo"}
    
@app.post("/users/{user_id}", Depends(oauth_scheme))
def create_user(user: User):
    
    return user

@app.get("/users/{user_id}")
def user(login: str, age: int, scores: List[float]):	
    return {"user_id": login, "age": age, "score": scores}

@app.get("/users/{User}/percentile")
async def percentile(user_score, k):
    k = len(user_score)
    percentile = np.percentile(k, user_score)
    return percentile


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host="127.0.0.1")