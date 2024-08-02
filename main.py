import uvicorn
from fastapi import FastAPI
from routers import auth, users

app = FastAPI()

app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(users.router, prefix='/users', tags=['users'])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8080,
        reload=True
    )
