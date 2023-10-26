from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import routers
from .routers import votes
# from .database.database import engine
# from .database.models import Base

# try:
#     Base.metadata.create_all(bind=engine)
#     print("db connected")
# except Exception as e:
#     print(f"db not connected --> {e}")


app = FastAPI(
    title="PostAPI", openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=routers.posts.router)
app.include_router(router=routers.users.router)
app.include_router(router=routers.auth.router)
app.include_router(router=votes.router)
