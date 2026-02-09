from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def app_start():
    return {"Message":"Server is Live"}