from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.interview import router

app = FastAPI(title="PSY AI-Powered Interview Engine")

# Enable CORS so your Next.js frontend can connect smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)