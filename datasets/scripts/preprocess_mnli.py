import csv, os, time
import numpy as np
import pandas as pd
import pandasql as ps
import time

filename = os.path.realpath("../multinli_1.0_train.csv")

# print("filename: " + filename)

f = pd.read_csv(filename)

# want to keep genre, gold_label, pairID, sentence1, sentence2
to_keep = ["pairID", "sentence1", "sentence2", "gold_label", "genre"]

df = f[to_keep]

# remove entries with neutral labels
# df = df[df.gold_label != "neutral"]
df2 = df.copy()
df2.rename(
    columns={
        "pairID": "Pair_id",
        "sentence1": "a",
        "sentence2": "b",
        "gold_label": "category",
        "genre": "subcategory",
    },
    inplace=True,
)


# Create dataset containing NLI pairs of the same relationships type (entailment, negation)
same_relation_df = df2[df2.category != "neutral"]

query = """
select distinct 
    t1.a, t1.b, t2.a as c, t2.b as d, t1.category, t1.subcategory as subcategory_1, t2.subcategory as subcategory_2
from
    same_relation_df t1
inner join same_relation_df t2
    on t1.category == t2.category
    and t1.subcategory == t2.subcategory
    and t1.a != t2.a
limit 10000000;
"""
print("running query")

t1 = time.perf_counter()
same_relation_result_df = ps.sqldf(query)
t2 = time.perf_counter()
print(f"Finished running in {t2 - t1:0.4f} seconds")


same_relation_result_df.to_csv("../mnli_relation_pairs.csv", index=False)