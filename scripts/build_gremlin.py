from gremlin_python.driver import client, serializer
import os
import dotenv
import sys
import asyncio
import time
import pandas as pd

dotenv.load_dotenv()

GREMLIN_URI = os.getenv("GREMLIN_URI")
GREMLIN_USER = os.getenv("GREMLIN_USER")
GREMLIN_PASSWORD = os.getenv("GREMLIN_PASSWORD")

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

local_client = client.Client(GREMLIN_URI, "g", username=GREMLIN_USER, password=GREMLIN_PASSWORD, message_serializer=serializer.GraphSONSerializersV2d0())

_DROP_DATABASE = "g.V().drop()"

def clear_database(local_client):
    local_client.submitAsync(_DROP_DATABASE)

def add_gene_vertice(local_client, gene_name):
    print(gene_name)
    _COMMAND = f"g.addV('gene').property('id', '{gene_name}').property('name', '{gene_name}').property('entity_type', 'gene').property('pk', 'pk')"
    local_client.submitAsync(_COMMAND)

def add_condition_vertice(local_client, condition_name):
    _COMMAND = f"g.addV('condition').property('id', '{condition_name}').property('name', '{condition_name}').property('entity_type', 'condition').property('pk', 'pk')"
    local_client.submitAsync(_COMMAND)

def add_drug_vertice():
    pass


def add_edge(local_client, parent, child):
    _COMMAND = f"g.V('{parent}').addE('links').to(g.V('{child}'))"
    local_client.submitAsync(_COMMAND)

"""
Rebuilt TRRUST Database on Gremlin
"""

TRRUST_FILEPATH = "static/data/v1/trrust_rawdata.human.tsv"

trrust_df = pd.read_csv(TRRUST_FILEPATH, delimiter="\t", header=None)
trrust_df.columns = ["TF", "TARGET", "RELATIONSHIP", "PUBMED_ID"]
print(trrust_df.head())

clear_database(local_client)

already_added_names = set()

for index, row in trrust_df.iterrows():
    if True:
        print(row["TF"], row["TARGET"])
        if row["TF"] not in already_added_names:
            add_gene_vertice(local_client, row["TF"])
            already_added_names.add(row["TF"])
        if row["TARGET"] not in already_added_names:
            add_gene_vertice(local_client, row["TARGET"])
            already_added_names.add(row["TARGET"])
        add_edge(local_client, row["TF"], row["TARGET"])
