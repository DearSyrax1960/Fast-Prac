import uvicorn
from fastapi import FastAPI, status
from routers import auth, users

app = FastAPI()

app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(users.router, prefix='/users', tags=['users'])


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return "server is running"


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8080,
        reload=True
    )
