# Python

# Pydantic

# FastAPI
from typing import List
from fastapi import FastAPI, status
from config import custom_openapi

# My imports
from models.Tweet import Tweet
from models.User import User


app = FastAPI()

# Path Operations

## Path Operations - User


### Create a User
@app.post(
    path='/users/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary='Register a User',
    tags=['Users']
)
def signup():
    pass

### Login User
@app.post(
    path='/users/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Login a User',
    tags=['Users']
)
def login():
    pass

### Show all Users
@app.get(
    path='/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary='Show all Users',
    tags=['Users']
)
def show_all_users():
    pass

### Show Users
@app.get(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Show User',
    tags=['Users']
)
def show_user():
    pass

# Update User
@app.put(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Update User',
    tags=['Users']
)
def update_user():
    pass

# Delete User
@app.delete(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Delete User',
    tags=['Users']
)
def delete_user():
    pass


##  Path Operations - Tweets

### Show all Tweets
@app.get(
    path='/',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary='Show all Tweets',
    tags=['Tweets']
)
def home():
    return {'Twitter API': 'Working'}

### Create a Tweet
@app.post(
    path='/tweets',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary='Post a Tweet',
    tags=['Tweets']
)
def create_tweet():
    pass

### Show a Tweet
@app.get(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Show a Tweet',
    tags=['Tweets']
)
def show_tweet():
    pass

### Delete a Tweet
@app.put(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Update a Tweet',
    tags=['Tweets']
)
def delete_tweet():
    pass

### Delete a Tweet
@app.delete(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Delete a Tweet',
    tags=['Tweets']
)
def delete_tweet():
    pass


# Custom OPEN API
app = custom_openapi(app)