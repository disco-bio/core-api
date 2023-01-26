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
from src import add_blank_vertice
from src import add_condition_vertice
from src import add_drug_vertice

dotenv.load_dotenv()

GREMLIN_URI = os.getenv("GREMLIN_URI")
GREMLIN_USER = os.getenv("GREMLIN_USER")
GREMLIN_PASSWORD = os.getenv("GREMLIN_PASSWORD")

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

local_client = client.Client(GREMLIN_URI, "g", username=GREMLIN_USER, password=GREMLIN_PASSWORD, message_serializer=serializer.GraphSONSerializersV2d0())

TRRUST_FILEPATH = "static/data/v1/trrust_rawdata.human.tsv"
CONDITION_TO_GENE_FILEPATH = "static/data/v1/processed_condition_to_gene.csv"
GENE_TO_DRUG_FILEPATH = "static/data/v1/drug.target.interaction.tsv"

trrust_df = pd.read_csv(TRRUST_FILEPATH, delimiter="\t", header=None)
trrust_df.columns = ["TF", "TARGET", "RELATIONSHIP", "PUBMED_ID"]
print(trrust_df.head())

cond_to_gene_df = pd.read_csv(CONDITION_TO_GENE_FILEPATH)
print(cond_to_gene_df.head())

raw_gene_to_drug_df = pd.read_csv(GENE_TO_DRUG_FILEPATH, delimiter='\t')
human_gene_to_drug_df = raw_gene_to_drug_df.loc[raw_gene_to_drug_df["ORGANISM"]=="Homo sapiens"]

try:
    already_added_names = set()

    # clear database
    print("clearing database...")
    clear_database.clear_database(local_client)
    
    # loop through TRRUST v2 database
    print("adding TRRUST v2 database...")

    for index, row in trrust_df.iterrows():
        if True:
            if row["TF"] not in already_added_names:
                add_gene_vertice.add_gene_vertice(local_client, row["TF"])
                already_added_names.add(row["TF"])
            if row["TARGET"] not in already_added_names:
                add_gene_vertice.add_gene_vertice(local_client, row["TARGET"])
                already_added_names.add(row["TARGET"])
            add_edge.add_edge(local_client, row["TF"], row["TARGET"])
            time.sleep(0.01)

    # add conditions
    print("adding conditions...")

    for index, row in cond_to_gene_df.iterrows():
        if index < 3000:
            if row["Disease Name"] not in already_added_names:
                add_condition_vertice.add_condition_vertice(local_client, row["Disease Name"])
                already_added_names.add(row["Disease Name"])
            if row["Gene ID"] not in already_added_names:
                add_gene_vertice.add_gene_vertice(local_client, row["Gene ID"])
                already_added_names.add(row["Gene ID"])
            add_edge.add_edge(local_client, row["Disease Name"], row["Gene ID"])
            time.sleep(0.01)

    # add drug interactions
    print("adding drug interactions...")

    for index, row in human_gene_to_drug_df.iterrows():
        if index < 3000:
            if row["GENE"] not in already_added_names:
                add_gene_vertice.add_gene_vertice(local_client, row["GENE"])
            if row["DRUG_NAME"] not in already_added_names:
                add_drug_vertice.add_drug_vertice(local_client, row["DRUG_NAME"])
                already_added_names.add(row["DRUG_NAME"])
            add_edge.add_edge(local_client, row["GENE"], row["DRUG_NAME"])
            time.sleep(0.01)

    # add blank node, as the last async call often emits a runtime error
    add_blank_vertice.add_blank_vertice(local_client)

except RuntimeError:
    print("skipped futures shutdown error")

print("completed script")
