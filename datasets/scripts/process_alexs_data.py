import pandas as pd

# TODO: BLiMP

# Language paper
for dataset in ["main_verb", "subject_aux_inversion"]:
    df = pd.read_json(f"../alexs_data/language_paper/{dataset}.jsonl", lines=True, orient="records")
    df = df[df["structural_label"]==1]
    df = df.rename({"sentence_base": "a", "sentence_transform": "b"}, axis=1)
    df = df.drop(["row", "structural_label", "surface_label"], axis=1)
    df.to_json(f"../alexs_data/final/{dataset}.jsonl", lines=True, orient="records")
    df = df[df["template"]=="1_RC_ambig_2"]
    df.to_json(f"../alexs_data/final/{dataset}_one_template.jsonl", lines=True, orient="records")

# MSGS
for dataset in ["relative_position", "title_case"]:
    df = pd.read_json(f"../alexs_data/msgs/{dataset}_control/test.jsonl", lines=True, orient="records")
    df["x"] = df.reset_index()["index"].apply(lambda x: x//2)
    df = df[["sentence", "surface_feature_label", "x"]]
    df1 = df[df["surface_feature_label"]==1].set_index("x").rename({"sentence": "a"}, axis=1)
    df0 = df[df["surface_feature_label"]==0].set_index("x").rename({"sentence": "b"}, axis=1)
    df = pd.concat([df1, df0], axis=1).drop("surface_feature_label", axis=1)
    df.to_json(f"../alexs_data/final/{dataset}.jsonl", lines=True, orient="records")


# FAVA
for dataset in ["dative", "spray_load", "there"]:
    df = pd.read_csv(f"../alexs_data/fava/{dataset}/all.tsv", sep="\t", header=None, names=["_", "label", "__", "sentence"])
    df = df[["label", "sentence"]]
    df["sentence"] = df["sentence"].apply(lambda s: s[0].upper() + s[1:-2] + ".")
    df["x"] = df.reset_index()["index"].apply(lambda x: x // 2)
    df["y"] = df.reset_index()["index"].apply(lambda x: x % 2)
    df1 = df[df["y"] == 1].set_index("x").rename({"sentence": "a", "label": "label_a"}, axis=1)
    df0 = df[df["y"] == 0].set_index("x").rename({"sentence": "b", "label": "grammatical"}, axis=1)
    df = pd.concat([df1, df0], axis=1).drop(["y", "label_a"], axis=1)
    df.to_json(f"../alexs_data/final/{dataset}_all.jsonl", lines=True, orient="records")
    df[df["grammatical"]==1].to_json(f"../alexs_data/final/{dataset}_grammatical.jsonl", lines=True, orient="records")



# df_abs_tok = pd.read_json(f"../alexs_data/msgs/absolute_token_position_control.jsonl", lines=True, orient="records")
# def fix_first_word(x):
#     dic =
#     if x.split()[0] == "The":
#         return x
#     else:
#         NOUN
#         FEWER
#         MORE
#         NO
#         ANY
#
#         {'Many': "Most",
#          'Every': "Every",
#          'An': "Every",
#          'This': "Every",
#          'Some': "Most",
#          'That': "Every",
#          'Those': "Most",
#          'These': "Most",
#          'Few': "Most",
#          'Each': "Every",
#          'Most': "Most",
#          'The': "The",
#          'A': "Every",
#          'All': "Most"}
