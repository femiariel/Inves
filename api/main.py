from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import api.db as db
from api.routes import universe, signals, proposal, backtest, portfolio, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(title="Alloc PEA", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

for mod in [universe, signals, proposal, backtest, portfolio, settings]:
    app.include_router(mod.router, prefix="/api")
