import uvicorn as uvicorn
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter, Request, FastAPI
from starlette.responses import PlainTextResponse

from utils import status_event_generator

app = FastAPI()

@app.get('/stream')
async def runStatus(
        param1: str,
        request: Request
):
    event_generator = status_event_generator(request, param1)
    return EventSourceResponse(event_generator)


@app.get('/test', response_class=PlainTextResponse, include_in_schema=False)
async def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # app.run(debug=True)
    uvicorn.run('main:app', port=8000, debug=True)
