from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from app.user.api import router as user_router
from app.flags.api import router as flags_router
from app.questions.api import router as questions_router
from app.responses.api import router as responses_router

app = FastAPI(
    title="TRP Backend API",
    description="Toronto Regional Properties Backend API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with new modular structure
app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(flags_router, prefix="/api/v1/flags", tags=["flags"])
app.include_router(questions_router, prefix="/api/v1/questions", tags=["questions"])
app.include_router(responses_router, prefix="/api/v1/responses", tags=["responses"])

@app.get("/")
async def root():
    return {"message": "TRP Backend API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 