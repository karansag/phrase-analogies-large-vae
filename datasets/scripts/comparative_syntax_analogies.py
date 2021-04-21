import csv
import pandas as pd

adjective = (
    "bad",
    "big",
    "bright",
    "cheap",
    "cold",
    "cool",
    "deep",
    "easy",
    "fast",
    "good",
    "great",
    "hard",
    "heavy",
    "high",
    "hot",
    "large",
    "long",
    "loud",
    "low",
    "new",
    # "old",
    "quick",
    "safe",
    "sharp",
    "short",
    "simple",
    "slow",
    "small",
    "smart",
    "strong",
    "tall",
    "tight",
    "tough",
    "warm",
    "weak",
    "wide",
    "young",
)

comparative = (
    "worse",
    "bigger",
    "brighter",
    "cheaper",
    "colder",
    "cooler",
    "deeper",
    "easier",
    "faster",
    "better",
    "greater",
    "harder",
    "heavier",
    "higher",
    "hotter",
    "larger",
    "longer",
    "louder",
    "lower",
    "newer",
    # "older",
    "quicker",
    "safer",
    "sharper",
    "shorter",
    "simpler",
    "slower",
    "smaller",
    "smarter",
    "stronger",
    "taller",
    "tighter",
    "tougher",
    "warmer",
    "weaker",
    "wider",
    "younger",
)


def remove_duplicates(phrase):
    output = []
    for x in phrase:
        if x not in output:
            output.append(x)
    return output


standardPhrase = ["a"]
comparativePhrase = ["b"]
with open("../snli_1.0_train.csv", newline="") as inputfile:
    for row in csv.reader(inputfile):
        word1 = ""
        word2 = ""

        valid_phrase1 = None
        valid_phrase2 = None

        thanPhrase1 = None
        thanPhrase2 = None

        cell1 = row[1].split()
        cell2 = row[2].split()

        i = 0

        while i < len(cell1):
            if cell1[i] in comparative:
                if (i + 1 < len(cell1) and cell1[i + 1] == "than") or (
                    i + 2 < len(cell1) and cell1[i + 2] == "than"
                ):
                    thanPhrase1 = True
                    if (cell1[i - 1])[-1] == ",":
                        cell1[i - 1] = str(cell1[i - 1]) + "which is "
                valid_phrase1 = True
                word1 = cell1[i]

            i += 1

        if bool(valid_phrase1):
            if row[1] in standardPhrase:
                pass
            else:
                standardPhrase.append(row[1])
                if thanPhrase1:
                    cell1 = cell1[: cell1.index("than")]
                cell1[cell1.index(word1)] = adjective[comparative.index(word1)]
                comparativePhrase.append(" ".join(cell1))

        i = 0

        while i < len(cell2):
            if cell2[i] in comparative:
                if (i + 1 < len(cell2) and cell2[i + 1] == "than") or (
                    i + 2 < len(cell2) and cell2[i + 2] == "than"
                ):
                    thanPhrase2 = True
                    if (cell2[i - 1])[-1] == ",":
                        cell2[i - 1] = str(cell2[i - 1]) + " which is "
                valid_phrase2 = True
                word2 = cell2[i]

            i += 1

        if bool(valid_phrase2):
            if row[2] in standardPhrase:
                pass
            else:
                standardPhrase.append(row[2])
                if thanPhrase2:
                    cell2 = cell2[: cell2.index("than")]
                cell2[cell2.index(word2)] = adjective[comparative.index(word2)]
                comparativePhrase.append(" ".join(cell2))

df = pd.DataFrame()
df["Original"] = standardPhrase
df["Modified"] = comparativePhrase
df.to_csv("../comparative_syntax_analogies.csv", sep=",", header=None, index=None)

print(".csv created with comparative syntactical analogies")
