from gremlin_python.driver import client, serializer
import os
import dotenv
import sys
import asyncio
import time

dotenv.load_dotenv()

GREMLIN_URI = os.getenv("GREMLIN_URI")
GREMLIN_USER = os.getenv("GREMLIN_USER")
GREMLIN_PASSWORD = os.getenv("GREMLIN_PASSWORD")

print(GREMLIN_URI)
print(GREMLIN_USER)
print(GREMLIN_PASSWORD)

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


local_client = client.Client(GREMLIN_URI, "g", username=GREMLIN_USER, password=GREMLIN_PASSWORD, message_serializer=serializer.GraphSONSerializersV2d0())

print(local_client)

DROP_DATABASE = "g.V().drop()"
INSERT_VERTICES = [
        "g.addV('person').property('id', 'thomas').property('firstName', 'Thomas').property('age', 44).property('pk', 'pk')",
        "g.addV('person').property('id', 'mary').property('firstName', 'Mary').property('age', 39).property('pk', 'pk')",
        "g.addV('person').property('id', 'ben').property('firstName', 'Ben').property('pk', 'pk')",
        "g.addV('person').property('id', 'robin').property('firstName', 'Robin').property('pk', 'pk')"
        ]


INSERT_EDGES = [
        "g.V('thomas').addE('knows').to(g.V('mary'))",
        "g.V('thomas').addE('knows').to(g.V('ben'))",
        "g.V('ben').addE('knows').to(g.V('robin'))"
        ]

callback = local_client.submitAsync(DROP_DATABASE)

for query in INSERT_VERTICES:
    callback = local_client.submitAsync(query)

for query in INSERT_EDGES:
    callback = local_client.submitAsync(query)
