
import random
from typing import List
import numpy as np
from fastapi import Depends, FastAPI, Path
from pydantic import BaseModel
import uvicorn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#initiate fast api
app = FastAPI()

#authorization layer
oauth_scheme = OAuth2PasswordBearer(tokenUrl= "token")

userdb = {}

@app.get("/")
def root():
    return {"Welcome to a fast api program that inherits data and stores it in a database which can be exposed via api functionality" , "Created by Abhishek Deorukhkar"}

#/token allows authorization viz oauth2 and keeps track of the authoirization and its validity
@app.post("/token")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    return {"access token":form_data.username, "Password" : form_data.password , "token_type": 'bearer', "expires_in": 600}


#will authorize whether the token is valid using the dependency being oauth_scheme
@app.get("/login")
async def login(token: str = Depends(oauth_scheme)):
    print(token)
    return {
        "username" : "user123",
        "password" : "1234"
    }
#should indicate the expiry of the authorization
@app.post("/expired")
async def expired():
    if token_generate.isExpired == True:
        return{
            "Authorization has expired, please sign in again!"
        }

# basemodel that specifies the parameters of User with the user id , age and the list of floating point numbers as scores
class User(BaseModel):
    id : str | None = None #= input('Please Enter A Name: ')
    age : int #= int(input('Please Enter An Age: '))
    score : List[float] =[]

#an endpoint where given the user id, will return data associted with the user - problem here is that I am unable to get the info on a given user_id
@app.get("/users/{user_id}")
def read_user(age: int, score: List[float], id: str = Path(title ="the id of the user")):	
    return {"user_id": id, "age": age, "score": score}

#create a new user and add them into the user list
@app.put("/users/{user_id}")
async def create_user(id: str = input("Please enter a Name: "), age: int = input("Please enter an Age: "), score:List[float] = [random.random()* 10, random.random()* 10, random.random()* 10, random.random()* 10, random.random()* 10], User = Depends(oauth_scheme)):
    return {"New User Created!: " : id, "Age": age, "Scores": score}

# get the k-th percentile of the list of floating point numbers and display it
@app.get("/users/{user_id}/percentile")
async def percentile():
    k = len(User.score)
    percentile = np.percentile(k, User.score)
    return percentile

#app inititation upon running the script; hosted on port 8000 as a defualt
if __name__ == '__main__':
    uvicorn.run(app, port=8000, host="127.0.0.1")