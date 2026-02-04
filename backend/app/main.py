from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.email_routes import router as email_router
from app.routes.auth_routes import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_router)
app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "Backend is healthy 🚀"}
