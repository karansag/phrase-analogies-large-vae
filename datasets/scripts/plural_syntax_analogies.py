import csv
import os
import random

import pandas as pd

singulars_list = (
    "banana",
    "bird",
    "bottle",
    "building",
    "car",
    "cat",
    "child",
    "cloud",
    "color",
    "computer",
    "cow",
    "dog",
    "dollar",
    "donkey",
    "dream",
    "eagle",
    "elephant",
    "eye",
    "finger",
    "goat",
    "hand",
    "horse",
    "kid",
    "lion",
    "machine",
    "man",
    "melon",
    "monkey",
    "mouse",
    "onion",
    "pear",
    "pig",
    "pineapple",
    "rat",
    "road",
    "snake",
    "student",
    "woman",
)

plurals_list = (
    "bananas",
    "birds",
    "bottles",
    "buildings",
    "cars",
    "cats",
    "children",
    "clouds",
    "colors",
    "computers",
    "cows",
    "dogs",
    "dollars",
    "donkeys",
    "dreams",
    "eagles",
    "elephants",
    "eyes",
    "fingers",
    "goats",
    "hands",
    "horses",
    "kids",
    "lions",
    "machines",
    "men",
    "melons",
    "monkeys",
    "mice",
    "onions",
    "pears",
    "pigs",
    "pineapples",
    "rats",
    "roads",
    "snakes",
    "students",
    "women",
)

third_person = (
    "is",
    "decreases",
    "describes",
    "does",
    "eats",
    "enhances",
    "estimates",
    "finds",
    "generates",
    "goes",
    "implements",
    "increases",
    "listens",
    "plays",
    "predicts",
    "provides",
    "says",
    "screams",
    "searches",
    "sees",
    "shuffles",
    "sings",
    "sits",
    "slows",
    "speaks",
    "swims",
    "talks",
    "thinks",
    "vanishes",
    "walks",
    "works",
    "writes",
    "rides",
    "zip",
    "hold",
)

normal_person = (
    "are",
    "decrease",
    "describe",
    "do",
    "eat",
    "enhance",
    "estimate",
    "find",
    "generate",
    "go",
    "implement",
    "increase",
    "listen",
    "play",
    "predict",
    "provide",
    "say",
    "scream",
    "search",
    "see",
    "shuffle",
    "sing",
    "sit",
    "slow",
    "speak",
    "swim",
    "talk",
    "think",
    "vanish",
    "walk",
    "work",
    "write",
    "ride",
    "zips",
    "holds",
)

indef_quant_list = (
    "",
    "some",
    "many",
    "two",
    "three",
    "four",
    "five",
    "six",
    "nine",
    "ten",
    "twenty",
    "twenty two",
    "one hundred",
    "two hundred",
)

def_quant_list = (
    "",
    "two",
    "three",
    "four",
    "five",
    "six",
    "nine",
    "ten",
    "twenty",
    "twenty two",
    "one hundred",
    "two hundred",
)

singular_phrase = ["a"]
plural_phrase = ["b"]
labels = ["category"]
sublabels = ["subcategory"]

with open("../snli_1.0_train.csv", newline="") as inputfile:
    for row in csv.reader(inputfile):
        word1 = []
        word2 = ""

        valid_phrase1 = None
        valid_phrase2 = None

        cell1 = row[4].split()
        cell2 = row[7].split()
        label = row[2]
        i = 0

        total_phrases_found = 0

        while i < len(cell1):
            if cell1[i] in singulars_list:
                valid_phrase1 = True
                word1.append(cell1[i])

            i += 1

        if bool(valid_phrase1):
            for singword in word1:

                temp1 = cell1

                temp1[cell1.index(singword)] = plurals_list[
                    singulars_list.index(singword)
                ]
                x = temp1.index(plurals_list[singulars_list.index(singword)])

                j = x

                while j < len(cell1):
                    # pos = wn.synsets(temp1[singword])[0].pos()
                    if temp1[j] in third_person:
                        temp1[j] = normal_person[third_person.index(cell1[j])]
                        break
                    j += 1

                if cell1[x - 1].lower() == "a" or cell1[x - 1].lower() == "one":
                    p = random.choice(indef_quant_list)
                    temp1[x - 1] = p

                    if (" ".join(temp1) in plural_phrase) and singular_phrase[
                        plural_phrase.index(" ".join(temp1))
                    ] == row[1]:
                        pass
                    singular_phrase.append(row[4])
                    plural_phrase.append(" ".join(temp1))
                    labels.append(label)
                    sublabels.append(
                        "{}|indefinite".format(p if len(p) > 0 else "various")
                    )
                if cell1[x - 1].lower() == "the":
                    p = random.choice(def_quant_list)
                    temp1.insert(x, p)

                    if (" ".join(temp1) in plural_phrase) and singular_phrase[
                        plural_phrase.index(" ".join(temp1))
                    ] == row[1]:
                        pass
                    singular_phrase.append(row[4])
                    plural_phrase.append(" ".join(temp1))
                    labels.append(label)
                    sublabels.append(
                        "{}|definite".format(p if len(p) > 0 else "various")
                    )

df = pd.DataFrame()
df["Original"] = singular_phrase
df["Modified"] = plural_phrase
df["Labels"] = labels
df["Sublabels"] = sublabels
print(df)
df.to_csv("../plural_sent_pairs.csv", sep=",", header=None, index=None)

print(".csv created with plural syntactical analogies")
