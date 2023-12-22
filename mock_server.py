import random
import time

from fastapi import Body, FastAPI, HTTPException, Request, status

app = FastAPI()


def is_success():
    result = random.randint(0, 100)
    wait_ms = random.randint(0, 600) / 1000.0
    time.sleep(wait_ms)
    return result <= 75


@app.get("/")
async def random_no_path(request: Request):
    if is_success():
        return {"message": f"Success! Path: '/'", "headers": request.headers}
    else:
        raise HTTPException(status_code=500, detail=f"Failure! Path: '/'")

@app.get("/{path}")
async def random_response(path: str, request: Request):
    if is_success():
        return {"message": f"Success! Path: '{path}'", "headers": request.headers}
    else:
        raise HTTPException(status_code=500, detail=f"Failure! Path: {path}")


@app.get("/status-no-content/{path}")
async def random_no_content(
    path: str, request: Request, status_code=status.HTTP_204_NO_CONTENT
):
    if is_success():
        return {"message": f"Success! Path: '{path}'", "headers": request.headers}
    else:
        raise HTTPException(status_code=500, detail=f"Failure! Path: {path}")


@app.post("/post-method/{path}")
async def random_post_method(
    path: str, request: Request, status_code=status.HTTP_201_CREATED
):
    if is_success():
        return {
            "message": f"Success! Path: '{path}'",
            "headers": request.headers,
            "body": await request.json(),
        }
    else:
        raise HTTPException(status_code=500, detail=f"Failure! Path: {path}")
