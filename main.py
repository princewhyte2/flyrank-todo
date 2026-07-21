from fastapi import FastAPI,HTTPException

app = FastAPI()

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


@app.get("/")
def read_root():
  return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def health_status():
  return {"status": "ok"}

@app.get("/tasks")
def tasks_list():
  return {"tasks":tasks}

@app.get("/tasks/{task_id}")
def single_task(task_id):
  for task in tasks :
    if task["id"] == int(task_id):
      return {"task":task}
  raise HTTPException(status_code=404 , detail = "Task " + task_id + " not found")