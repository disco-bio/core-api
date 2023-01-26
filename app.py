from gremlin_python.driver import client, serializer

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import JSONResponse
import uvicorn

from src import gremlin_list_conditions
from src import add_blank_vertice

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

@app.get("/")
async def home():
    data = {"data": "Disco API"}
    return JSONResponse(data)

@app.get("/get_list_conditions")
def get_list_conditions():
    return_data = {"data": []}

    callback = gremlin_list_conditions.gremlin_list_conditions(local_client)
    _ = add_blank_vertice.add_blank_vertice(local_client)
    
    for item in callback.result().all().result():
        return_data["data"].append(item["objects"][0]["id"])


    return return_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
