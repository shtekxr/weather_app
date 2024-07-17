import os

import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.routers import router
from src.database import init_db

app = FastAPI(title="Weather App")


@app.on_event("startup")
async def on_startup():
    init_db()


app.include_router(router)

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../static")), name="static")


templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "../templates"))


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == '__main__':
    '''Server'''
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
