import uvicorn
from fastapi import FastAPI
from routers import auth

app = FastAPI()

app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8080,
        reload=True
    )
