import uvicorn
from fastapi import FastAPI
from chat.routers import chat

app = FastAPI()

# Routers
app.include_router(chat.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, workers=1)
