from fastapi import FastAPI, Path, status, Body, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users")
async  def users_get() -> List[User]:
    return users

@app.post("/user/{username}/{age}")
async def users_post(user: User, username: str, age: int) -> User:
    user.id = len(users) +1
    users.append(user)
    user.username = username
    user.age = age
    return user


@app.put("/user/{id}/{username}/{age}")
async def users_put(user: User, id: int, username: str, age: int) -> User:
    try:
        user.id = id -1
        user = users[user.id]
        user.username = username
        user.age = age
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete('/user/{id}')
async def users_delete(user: User, id: int) -> str:
    try:
        user.id = id -1
        users.pop(user.id)
        return f"User {id} has been deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")

if __name__ == '__main__':
    uvicorn.run(app="CRUD2:app", reload=True)