from fastapi import FastAPI
from routes.contacts import router as contacts_router
from routes.auth import router as auth_router


app = FastAPI()

app.include_router(contacts_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "contacts on FastAPI"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
