import csv, os, time
import numpy as np
import pandas as pd
import pandasql as ps
import time

filename = os.path.realpath("../multinli_1.0_train.csv")

f = pd.read_csv(filename)

# want to keep genre, gold_label, pairID, sentence1, sentence2
to_keep = ["pairID", "sentence1", "sentence2", "gold_label", "genre"]

df = f[to_keep]

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

df2.to_csv("../mnli_cleaned.csv", index=False)