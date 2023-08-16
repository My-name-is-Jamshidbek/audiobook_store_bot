from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running"}

@app.get("/pay")
def process_data():
    return RedirectResponse(url = "https://t.me/mal_un")