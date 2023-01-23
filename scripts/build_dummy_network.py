from bson.objectid import ObjectId as bsonObjectId
import pymongo
import dotenv
import os
import pandas as pd
from pprint import pprint


dotenv.load_dotenv()

# load dummy datasets

disease_to_gene_df = pd.read_csv("static/data/dummy-data/disease-to-gene.csv")
print(disease_to_gene_df.head())

entrez_to_gene_df = pd.read_csv("static/data/dummy-data/entrez-to-gene.csv")
print(entrez_to_gene_df.head())

gene_to_gene_df = pd.read_csv("static/data/dummy-data/gene-to-gene.csv")
print(gene_to_gene_df.head())

gene_to_drug_df = pd.read_csv("static/data/dummy-data/gene-to-drug.csv")
print(gene_to_drug_df.head())


client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
client.drop_database("test-db-1")

print(client)


def create_list_of_json_for_entrez_to_gene(df):
    return_list = []
    for index, row in df.iterrows():
        return_list.append({"entrez_code": row["entrez_gene"], "gene_symbol": row["gene_symbol"]})
    return return_list

entrez_to_gene_list = create_list_of_json_for_entrez_to_gene(entrez_to_gene_df)

pprint(entrez_to_gene_list)

client["test-db-1"]["entrez-to-gene"].insert_many(entrez_to_gene_list)



def entrez_to_gene(df, entrez_id):
    """
    entrez-to-gene mapping function
    """
    result = client["test-db-1"]["entrez-to-gene"].find_one({"entrez_code":entrez_id})
    return result["gene_symbol"]
    
print(entrez_to_gene(entrez_to_gene_df, "e1"))
