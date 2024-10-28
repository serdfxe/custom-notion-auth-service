from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router


def init_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def init_routers(app: FastAPI) -> None:
    app.include_router(router)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Auth Service",
        description="Hide API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    init_routers(app=app)
    init_cors(app=app)
    
    return app


app = create_app()