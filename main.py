from searcher import Searcher
from trie import Trie
from helper import parse_query, make_response, download_from_bucket

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

import settings
import os
import time

trie = Trie()
searcher = Searcher(trie)
app = FastAPI(title="Object Search")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    error_details = []

    for error in details:
        error_details.append({"error": f"{error['msg']} {str(error['loc'])}"})

    return make_response(status=200, message="Bad Request", data=error_details)


@app.get("/", include_in_schema=False)
async def root() -> None:
    return RedirectResponse("/docs")


@app.get("/health", status_code=status.HTTP_200_OK, tags=["health"])
async def perform_healthcheck() -> None:
    return make_response(status=200, message="OK")


class Query(BaseModel):
    query_text: str
    topk: int


@app.post("/search", status_code=status.HTTP_200_OK, tags=["search"])
async def search(query: Query) -> None:
    topk = query.topk
    query = parse_query(query.query_text)

    candidates = searcher.search(query, topk)
    data = [candidate.serialize() for candidate in candidates]
    return make_response(status=200, message="OK", data=data)


@app.on_event("startup")
async def startup_event():
    if os.path.exists("cache.json"):
        start_time = time.time()
        trie.load_from_cache("cache.json")
        print("Load from cache took %.2f seconds" % (time.time() - start_time))
    else:
        if not os.path.exists("data"):
            os.mkdir("data")
            start_time = time.time()
            download_from_bucket("data")
            print("Download from bucket took %.2f seconds" % (time.time() - start_time))
        start_time = time.time()
        trie.load_from_dir("data")
        trie.save_to_cache("cache.json")
        print("Load from directory took %.2f seconds" % (time.time() - start_time))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
