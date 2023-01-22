import pymongo
import dotenv
import os
import pandas as pd

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
print(client)
