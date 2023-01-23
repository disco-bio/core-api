import pandas as pd
import json

CONDITION_TO_GENE_FILEPATH = "static/data/v1/condition-to-gene.tsv"
ENTREZ_TO_GENE_FILEPATH = "static/data/v1/entrez_to_gene.json"

cond_to_gene_df = pd.read_csv(CONDITION_TO_GENE_FILEPATH, delimiter="\t")
print(cond_to_gene_df.head())

# <str> -> <str> mapping
entrez_to_gene_dict = json.load(open(ENTREZ_TO_GENE_FILEPATH, "r"))

def map_entrez_to_gene(entrez_code):
    if str(entrez_code) in entrez_to_gene_dict.keys():
        return entrez_to_gene_dict[str(entrez_code)]
    else:
        return None

cond_to_gene_df["Gene ID"] = cond_to_gene_df["Gene ID"].apply(map_entrez_to_gene)

print(cond_to_gene_df.head())

nan_count = cond_to_gene_df["Gene ID"].isna().sum()
print(nan_count)
print(cond_to_gene_df.shape)
cond_to_gene_df = cond_to_gene_df.dropna()
cond_to_gene_df.to_csv("processed_condition_to_gene.csv")
