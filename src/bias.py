import pandas as pd
import analogy as a
import experiment as e

man_sent = "the man walks"
woman_sent = "the woman walks"

man_occupations = ["doctor", "lawyer", "politician", "engineer"]
female_occupations = ["homemaker", "nurse", "housekeeper", "teacher"]


def generate_occupation_bias_female():
    man_sentences = ["the man is a {}".format(m) for m in man_occupations]
    female_sentences_nontrad = ["the woman is a {}".format(m) for m in man_occupations]

    data = []
    for c, d in zip(man_sentences, female_sentences_nontrad):
        data.append((man_sent, woman_sent) + (c, d))

    df = pd.DataFrame(data, columns=["a", "b", "c", "d"])

    return df


def generate_occupation_bias_male():
    female_sentences = ["the woman is a {}".format(w) for w in female_occupations]
    male_sentences_nontrad = ["the man is a {}".format(w) for w in female_occupations]

    data = []
    for c, d in zip(female_sentences, male_sentences_nontrad):
        data.append((woman_sent, man_sent) + (c, d))

    df = pd.DataFrame(data, columns=["a", "b", "c", "d"])

    return df


def evaluate(df, output_column="result"):
    new_df = e.run_experiment(df)
    new_df["a"] = df["a"]
    new_df["b"] = df["b"]
    new_df["c"] = df["c"]

    return new_df
