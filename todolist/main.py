from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI()

class Item:
    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description

class TodoListManager:
    def __init__(self):
        self.todo_list: List[Item] = []
        self.item_count = 0

    def add_todo(self, todo: str):
        self.item_count += 1
        self.todo_list.append(Item(self.item_count, todo))
        return self.todo_list

    def remove_todo(self, id: int):
        for item in self.todo_list:
            if item.id == id:
                self.todo_list.remove(item)
                return {"message": f"Item {id} removed successfully"}
        raise HTTPException(status_code=404, detail="Item not found")

    def update_todo(self, id: int, todo: str):
        for item in self.todo_list:
            if item.id == id:
                item.description = todo
                return {"message": f"Item {id} updated successfully"}
        raise HTTPException(status_code=404, detail="Item not found")

todo_manager = TodoListManager()

@app.get("/")
def todolist():
    return todo_manager.todo_list

@app.get("/add/{todo}")
def add_todo(todo: str):
    return todo_manager.add_todo(todo)

@app.get("/delete/{id}")
def remove_todo(id: int):
    return todo_manager.remove_todo(id)

@app.get("/update/{id}/{todo}")
def update_todo(id: int, todo: str):
    return todo_manager.update_todo(id, todo)
