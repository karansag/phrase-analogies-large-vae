import csv
import os
import random

import pandas as pd

singulars_list = ("banana",
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
                  "woman")

plurals_list = ("bananas",
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

third_person = ("is", "decreases",
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
                "hold"
                )

normal_person = ("are", "decrease",
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
                 "holds"
                 )

indef_quant_list = ("",
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
                    "two hundred")

def_quant_list = ("",
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
                  "two hundred")

singular_phrase = ["a"]
plural_phrase = ["b"]

with open(os.path.dirname(__file__) + '/snli_1.0_train.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        word1 = []
        word2 = ""

        valid_phrase1 = None
        valid_phrase2 = None

        cell1 = row[1].split()
        cell2 = row[2].split()

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

                temp1[cell1.index(singword)] = plurals_list[singulars_list.index(singword)]
                x = temp1.index(plurals_list[singulars_list.index(singword)])

                j = x

                while j < len(cell1):
                    # pos = wn.synsets(temp1[singword])[0].pos()
                    if temp1[j] in third_person:
                        temp1[j] = normal_person[third_person.index(cell1[j])]
                        break
                    j += 1

                if cell1[x - 1].lower() == "a" or cell1[x - 1].lower() == "one":
                    temp1[x - 1] = random.choice(indef_quant_list)

                    if (" ".join(temp1) in plural_phrase) and singular_phrase[
                        plural_phrase.index(" ".join(temp1))] == row[1]:
                        pass
                    singular_phrase.append(row[1])
                    plural_phrase.append(" ".join(temp1))
                if cell1[x - 1].lower() == "the":
                    temp1.insert(x, random.choice(def_quant_list))
                    if (" ".join(temp1) in plural_phrase) and singular_phrase[
                        plural_phrase.index(" ".join(temp1))] == row[1]:
                        pass
                    singular_phrase.append(row[1])
                    plural_phrase.append(" ".join(temp1))

df = pd.DataFrame()
df["Original"] = singular_phrase
df["Modified"] = plural_phrase
df.to_csv(os.path.dirname(__file__) + 'plural_sent_pairs.csv', sep=",", header=None, index=None)

print(".csv created with plural syntactical analogies")
