from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Import routers from modules
from modules.properties.search.search import router as search_router
from modules.properties.get.get import router as get_router
from modules.properties.media.media import router as media_router
from modules.users.authentication.auth import router as auth_router
from modules.page_load.home.home import router as home_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="TRP Backend API",
    description="Toronto Regional Properties Backend API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(search_router)
app.include_router(get_router)
app.include_router(media_router)
app.include_router(auth_router)
app.include_router(home_router)

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "TRP Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 