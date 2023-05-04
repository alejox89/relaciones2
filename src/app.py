from fastapi import FastAPI
from routes.llaveros import llavero
import logging
from http import HTTPStatus
from fastapi import FastAPI, Request, Response
from starlette.background import BackgroundTask
from starlette.types import Message
from fastapi.routing import APIRoute
from typing import Optional
import requests


app = FastAPI()
logging.basicConfig( filename='log_file_name.log',
                    level=logging.INFO, 
                    format='%(asctime)s.%(msecs)03d- %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
status_reasons = {x.value:x.name for x in list(HTTPStatus)}

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s.%(msecs)03d- %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

def log_info(req_body, res_body, informacion):
    logging.info(req_body)
    logging.info(res_body)
    logging.info(informacion)

async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {'type': 'http.request', 'body': body}
    request._receive = receive
    
@app.middleware('http')
async def some_middleware(request: Request, call_next):
    req_body = await request.body()
    await set_body(request, req_body)
    response = await call_next(request)
    
    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk
    
    informacion = {"Respuesta: " + status_reasons.get(response.status_code), "URL: "+request.url.path, "Metodo: "+ request.method, 
                   "Headers: " + str(request.headers)}
    
    task = BackgroundTask(log_info, req_body, res_body, informacion)
    return Response(content=res_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type, background=task)
    

app.include_router(llavero)