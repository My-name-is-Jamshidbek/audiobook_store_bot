from fastapi import FastAPI
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# Add middleware for HTTPS redirection
app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with HTTPS!"}
