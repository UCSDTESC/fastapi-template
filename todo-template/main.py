# Importing necessary modules from FastAPI and typing for type hinting
from fastapi import FastAPI, HTTPException
from typing import List

# Creating an instance of FastAPI
app = FastAPI()

# Defining a class 'Item' to represent each todo item
class Item:
    # Constructor to initialize the attributes of the item
    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description

# Todo list to store all the todos, initialized as an empty list
todo_list: List[Item] = []

# Variable to keep track of the total number of items
item_count = 0

# Endpoint to handle GET requests to the root URL "/"
@app.get("/")
def todolist():
    # Returns the list of todo items
    return todo_list

# Endpoint to handle GET requests with a message parameter for adding a new todo item
@app.get("/add/{todo}")
def add_todo(todo: str):
    # Using the global keyword to access and modify the global variable 'item_count'
    global item_count
    # Incrementing the item count to generate a unique ID for the new item
    item_count += 1
    # Creating a new Item object with the generated ID and provided description and add to the todo list
    todo_list.append(Item(item_count, todo))
    # Returning the updated todo list
    return todo_list

# Endpoint to handle GET requests with an ID parameter for removing a todo item
@app.get("/delete/{id}")
def remove_todo(id: int):
    # Using the global keyword to access and modify the global variables 'todo_list' and 'item_count'
    global todo_list
    global item_count
    # Iterating through each item in the todo list
    for item in todo_list:
        # Checking if the ID of the current item matches the provided ID
        if item.id == id:
            # Removing the item from the todo list
            todo_list.remove(item)
            # Returning a success message indicating the item removal
            return {"message": f"Item {id} removed successfully"}
    # If no item with the provided ID is found, raising an HTTPException with a status code of 404
    raise HTTPException(status_code=404, detail="Item not found")
