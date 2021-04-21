import csv, os, time
import numpy as np
import pandas as pd
from tqdm import tqdm


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
same_relation_result_df = pd.DataFrame(
    columns=["a", "b", "c", "d", "category", "subcategory_1", "subcategory_2"]
)

for i, row in tqdm(same_relation_df.iterrows(), total=len(same_relation_df.index)):
    time.sleep(0.01)
    curr_category = row["category"]
    curr_genre = row["subcategory"]

    new_rows = []
    # select 5 other random rows with same category and genre (subcategory)
    # select 5 other random rows with same category and different genre (subcategory)
    same_cat_same_genre = same_relation_df[
        np.logical_and(
            same_relation_df.category == curr_category,
            same_relation_df.subcategory == curr_genre,
        )
    ].sample(5)
    same_cat_diff_genre = same_relation_df[
        np.logical_and(
            same_relation_df.category == curr_category,
            same_relation_df.subcategory != curr_genre,
        )
    ].sample(5)

    for j, val in same_cat_same_genre.iterrows():
        new_rows.append(
            pd.Series(
                [
                    row["a"],
                    row["b"],
                    val["a"],
                    val["b"],
                    curr_category,
                    curr_genre,
                    val["subcategory"],
                ],
                index=same_relation_result_df.columns,
            )
        )

    for j, val in same_cat_diff_genre.iterrows():
        new_rows.append(
            pd.Series(
                [
                    row["a"],
                    row["b"],
                    val["a"],
                    val["b"],
                    curr_category,
                    curr_genre,
                    val["subcategory"],
                ],
                index=same_relation_result_df.columns,
            )
        )

    same_relation_result_df = same_relation_result_df.append(
        new_rows, ignore_index=True
    )

same_relation_result_df.to_csv("mnli_relation_pairs.csv", index=False)