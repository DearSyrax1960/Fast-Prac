import uvicorn
from fastapi import FastAPI
from views import auth, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8080,
        reload=True
    )
