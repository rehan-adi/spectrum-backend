from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI();

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

# Health Check Route
@app.get("/", status_code=200)
async def health_check():
    """
    Health check route to ensure the server is running.
    Returns a 200 OK status with a message.
    """
    return {"status": "healthy", "message": "Server is running!"}