from fastapi import FastAPI,HTTPException,Response,status
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
  title:str | None = None
  done: bool = False

tasks = [{
  "id": 1,
  "title":"Complete a backend Task",
  "done": True
},
{
  "id": 2,
  "title":"Build My betoracle v3",
  "done": False
},
{
  "id": 3,
  "title":"Call family members",
  "done": False
}
]


@app.get("/", summary='Read root')
def read_root():
  return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health", summary='Health Status')
def health_status():
  return {"status": "ok"}

@app.get("/tasks", summary='Get all Tasks')
def tasks_list():
  return {"tasks":tasks}

@app.get("/tasks/{task_id}", summary='Get task by Id')
def single_task(task_id):
  for task in tasks :
    if task["id"] == int(task_id):
      return {"task":task}
  raise HTTPException(status_code=404 , detail = "Task " + task_id + " not found")

@app.post("/tasks",status_code=status.HTTP_201_CREATED, summary='Create a new Task')
def create_task(task: Task, response:Response):
  if not task.title:
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"error": "title is required"}

  new_task = {
    "title":task.title,
    "id": len(tasks) + 1,
    "done": False
  }
  tasks.append(new_task)
  return {"task":new_task}

@app.put("/tasks/{task_id}",summary='Update an existing Task')
def update_task(task_id: int , task:Task):
  if task.title is None and task.done is None:
    raise HTTPException(status_code=400 , detail = "Empty/invalid body")
  for index, task_item in enumerate(tasks):
    if task_id == task_item["id"]:
      task_copy = task_item.copy()
      task_to_update = task.model_dump(exclude_unset=True)
      task_copy.update(task_to_update)
      tasks[index] = task_copy
      return {"task": tasks[index]}
  raise HTTPException(status_code=404 , detail = "Unknown id")

@app.delete("/tasks/{task_id}",status_code=status.HTTP_204_NO_CONTENT,summary='Delete an existing task')
def delete_task(task_id:int):
  for index,task_item in enumerate(tasks):
    if task_id == task_item["id"]:
      del tasks[index]
      return {}
  raise HTTPException(status_code=404 , detail = "Unknown id")