from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import database

# Létrehozzuk az adatbázis táblákat, ha még nem léteznek
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Adatbázis-alapú To-Do API", version="1.0")

from pydantic import BaseModel

# Pydantic séma a bejövő adatok validálásához
class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TodoResponse(TodoCreate):
    id: int

    class Config:
        from_attributes = True

# 1. Összes feladat lekérdezése az adatbázisból
@app.get("/todos", response_model=list[TodoResponse])
def get_todos(db: Session = Depends(database.get_db)):
    todos = db.query(models.TodoModel).all()
    return todos

# 2. Új feladat mentése az adatbázisba
@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(database.get_db)):
    db_todo = models.TodoModel(
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# 3. Feladat törlése ID alapján
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(database.get_db)):
    db_todo = db.query(models.TodoModel).filter(models.TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="A feladat nem található")
    db.delete(db_todo)
    db.commit()
    return {"message": "A feladat sikeresen törölve"}