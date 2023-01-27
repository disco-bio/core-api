from gremlin_python.driver import client, serializer

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uvicorn

from src import gremlin_list_conditions
from src import add_blank_vertice
from src import traverse_from_condition_until_drug

import dotenv
import asyncio

import sys
import os

dotenv.load_dotenv()


GREMLIN_URI = os.getenv("GREMLIN_URI")
GREMLIN_USER = os.getenv("GREMLIN_USER")
GREMLIN_PASSWORD = os.getenv("GREMLIN_PASSWORD")


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


local_client = client.Client(GREMLIN_URI, "g", username=GREMLIN_USER, password=GREMLIN_PASSWORD, message_serializer=serializer.GraphSONSerializersV2d0())

app = FastAPI()


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    data = {"data": "Disco API"}
    return templates.TemplateResponse("home.html", {"request": request, "title": "Title"})
    # return JSONResponse(data)

@app.get("/api/v0/get_list_conditions")
def get_list_conditions():
    return_data = {"data": []}

    callback = gremlin_list_conditions.gremlin_list_conditions(local_client)
    _ = add_blank_vertice.add_blank_vertice(local_client)
    
    for item in callback.result().all().result():
        return_data["data"].append(item["objects"][0]["id"])


    return return_data

@app.get("/api/v0/get_treatment_for", response_class=HTMLResponse)
def get_treatment_for(request: Request, q: str = None):
    return_data = {"data": []}

    callback = traverse_from_condition_until_drug.traverse_from_condition_until_drug(local_client, q)
    _ = add_blank_vertice.add_blank_vertice(local_client)

    for item in callback.result().all().result():
        return_data["data"].append(item["id"])

    # return return_data

    return templates.TemplateResponse("response.html", {"request": request, "data": return_data})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
