from gremlin_python.driver import client, serializer
import os
import dotenv
import sys
import asyncio
import time
import pandas as pd

from src import clear_database
from src import add_edge
from src import add_gene_vertice


dotenv.load_dotenv()

GREMLIN_URI = os.getenv("GREMLIN_URI")
GREMLIN_USER = os.getenv("GREMLIN_USER")
GREMLIN_PASSWORD = os.getenv("GREMLIN_PASSWORD")

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

local_client = client.Client(GREMLIN_URI, "g", username=GREMLIN_USER, password=GREMLIN_PASSWORD, message_serializer=serializer.GraphSONSerializersV2d0())

TRRUST_FILEPATH = "static/data/v1/trrust_rawdata.human.tsv"

trrust_df = pd.read_csv(TRRUST_FILEPATH, delimiter="\t", header=None)
trrust_df.columns = ["TF", "TARGET", "RELATIONSHIP", "PUBMED_ID"]
print(trrust_df.head())

try:
    already_added_names = set()

    clear_database.clear_database(local_client)
    for index, row in trrust_df.iterrows():
        if index < 20:
            if row["TF"] ont in already_added_names:
                add_gene_vertice(local_client, row["TF"])
                already_added_names.add(row["TF"])
            if row["TARGET"] not in already_added_names:
                add_gene_vertice(local_client, row["TARGET"])
                already_added_names.add(row["TARGET"])
            add_edge(local_client, row["TF"], row["TARGET"])
    clear_database.clear_database(local_client)
except:
    print("skipped futures shutdown error")

print("going on here")
