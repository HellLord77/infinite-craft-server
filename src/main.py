import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.orm import Session

import config
import init
from crud import get_result
from dependencies import get_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init.load_database()
    yield
    init.close_database()


app = FastAPI(debug=config.DEBUG_FASTAPI, lifespan=lifespan)
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=(config.CORS_ALLOW_ORIGIN,),
    allow_methods=(config.CORS_ALLOW_METHOD,),
    allow_headers=(config.CORS_ALLOW_HEADER,),
)
# noinspection PyTypeChecker
app.add_middleware(GZipMiddleware)


@app.get("/pair")
def pair(first: str, second: str, db: Session = Depends(get_db)):
    return get_result((first, second), db)


@app.middleware("http")
async def add_process_time_header_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.perf_counter() - start_time)
    return response


def main():
    uvicorn.run(app)


if __name__ == "__main__":
    main()
