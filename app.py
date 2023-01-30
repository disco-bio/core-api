from gremlin_python.driver import client, serializer

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uvicorn

from src import gremlin_list_conditions
from src import add_blank_vertice
from src import traverse_from_condition_until_drug
from src import translate
from src import quantum_bundle

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
def home(request: Request, lang: str=None):
    data = {"data": "Disco API"}
    if lang is None:
        return templates.TemplateResponse("home.html", {"request": request, "lang": "en"})
    else:
        return templates.TemplateResponse("home.html", {"request": request, "lang": lang})


@app.get("/api/v0/homepage_content")
def api_homepage_content(request: Request, lang: str=None):

    content_dict = {
            "subtitle": "A Drug Discovery Platform",
            "search_button": "Search"
        }


    if lang is not None or lang!="en":
        for key_ in content_dict.keys():
            content_dict[key_] = translate.translate(
                text=content_dict[key_],
                language_to=lang)[0]["translations"][0]["text"]

    return JSONResponse(content_dict)


@app.get("/api/v0/results_content")
def api_results_content(request: Request, lang: str=None):

    content_dict = {
            "title": "Search Results",
            "quantumSubtitle": "Quantum-Based Recommendation: "
        }


    if lang is not None or lang!="en":
        for key_ in content_dict.keys():
            content_dict[key_] = translate.translate(
                text=content_dict[key_],
                language_to=lang)[0]["translations"][0]["text"]

    return JSONResponse(content_dict)


@app.get("/api/v0/get_list_conditions")
def get_list_conditions():
    return_data = {"data": []}

    callback = gremlin_list_conditions.gremlin_list_conditions(local_client)
    _ = add_blank_vertice.add_blank_vertice(local_client)
    
    for item in callback.result().all().result():
        return_data["data"].append(item["objects"][0]["id"])

    return return_data


@app.get("/api/v0/get_treatment_for", response_class=HTMLResponse)
def get_treatment_for(request: Request, q: str = None, lang: str=None):

    return templates.TemplateResponse("response.html", {"request": request, "q": q, "lang": lang})



@app.get("/api/v0/get_data_for")
def get_data_for(q: str = None):
    return_data = {"data": [], "quantumResult": None}


    callback = traverse_from_condition_until_drug.traverse_from_condition_until_drug(local_client, q)

    items = callback.result().all().result()

    for item in items:

        print(item)

        sub_dict = {
                "drugName": None,
                "pubmedUrl": None,
            }

        sub_dict["drugName"] = item["id"]
        sub_dict["pubmedUrl"] = f"https://pubmed.ncbi.nlm.nih.gov/?term={item['id']}"

        return_data["data"].append(sub_dict)


    callback = traverse_from_condition_until_drug.list_results_path(local_client, q)

    print(callback.result().all().result())

    _ = add_blank_vertice.add_blank_vertice(local_client)


    # insert 


    res = quantum_bundle.compute_result(items)
    print(res)

    return_data["quantumResult"] = res


    return JSONResponse(return_data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
