from fastapi import FastAPI, HTTPException, Form, Header
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {}

@app.get("/miscellaneous/addition")
def addition(a: int, b: int):
    return {"result": a + b}

class User(BaseModel):
    username: str
    password: str

class TodoItem(BaseModel):
    name: str
    description: str
    priority: int

class TodoItemWithID(TodoItem):
    id: int
    username: str  # Ajout de l’attribut `username` pour lier chaque TODO à un utilisateur

users_db = {}
todos_db = {}
next_id = 1

@app.post("/users", status_code=201)
def create_user(user: User):
    users_db[user.username] = user
    return {"username": user.username, "todo_count": 0}

@app.post("/token")
def login(username: str = Form(...), password: str = Form(...)):
    if username not in users_db or users_db[username].password != password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"access_token": username}

@app.get("/users/me")
def get_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")  # Extraire le token de l'en-tête `Authorization`
    if token not in users_db:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = users_db[token]
    return {
        "username": user.username,
        "todo_count": len([todo for todo in todos_db.values() if todo.username == user.username])
    }

@app.post("/users/me/todo", response_model=TodoItemWithID, status_code=201)
def create_todo(todo: TodoItem, authorization: str = Header(...)):
    global next_id
    token = authorization.replace("Bearer ", "")
    if token not in users_db:
        raise HTTPException(status_code=400, detail="Invalid token")
    todo_with_id = TodoItemWithID(id=next_id, username=token, **todo.dict())
    todos_db[next_id] = todo_with_id
    next_id += 1
    return todo_with_id

@app.get("/users/me/todo", response_model=list[TodoItemWithID])
def get_todos(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    if token not in users_db:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_todos = [todo for todo in todos_db.values() if todo.username == token]
    return sorted(user_todos, key=lambda x: x.priority)

@app.patch("/users/me/todo/{id}", response_model=TodoItemWithID)
def update_todo(id: int, todo: TodoItem, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    if token not in users_db:
        raise HTTPException(status_code=400, detail="Invalid token")
    if id not in todos_db or todos_db[id].username != token:
        raise HTTPException(status_code=404, detail="TODO item not found or unauthorized")
    updated_todo = todos_db[id].copy(update=todo.dict())
    todos_db[id] = updated_todo
    return updated_todo

@app.delete("/users/me/todo/{id}", status_code=204)
def delete_todo(id: int, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    if token not in users_db:
        raise HTTPException(status_code=400, detail="Invalid token")
    if id not in todos_db or todos_db[id].username != token:
        raise HTTPException(status_code=404, detail="TODO item not found or unauthorized")
    del todos_db[id]
    return {"message": "TODO item deleted successfully"}
