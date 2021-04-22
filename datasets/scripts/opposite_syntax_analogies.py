import csv
import pandas as pd
import os

wordList = ("acceptable",
            "aware",
            "certain",
            "clear",
            "comfortable",
            "competitive",
            "consistent",
            "convenient",
            "convincing",
            "decided",
            "efficient",
            "ethical",
            "fortunate",
            "honest",
            "impressive",
            "informative",
            "informed",
            "known",
            "likely",
            "logical",
            "pleasant",
            "possible",
            "possibly",
            "productive"
            "rational"
            "reasonable"
            "responsible"
            "sure"
            "tasteful")

oppositeList = ("unacceptable",
                "unaware",
                "uncertain",
                "unclear",
                "uncomfortable",
                "uncompetitive",
                "inconsistent",
                "inconvenient",
                "unconvincing",
                "undecided",
                "inefficient",
                "unethical",
                "unfortunate",
                "dishonest",
                "unimpressive",
                "uninformative",
                "uninformed",
                "unknown",
                "unlikely",
                "illogical",
                "unpleasant",
                "impossible",
                "impossibly",
                "unproductive"
                "irrational"
                "unreasonable"
                "irresponsible"
                "unsure"
                "distasteful")

original = []
oppositeSentences = []

pair_a = []
pair_b = []
gold_label = []

with open(os.path.dirname(__file__) + '/snli_1.0_train.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        word1 = ""
        word2 = ""

        valid_phrase1 = None
        valid_phrase2 = None

        cell1 = row[1].split()
        cell2 = row[2].split()
        for word in wordList:
            if word in cell1:
                valid_phrase1 = True
                word1 = word

        if bool(valid_phrase1):
            if row[1] in original:
                pass
            else:
                original.append(row[1])
                cell1[cell1.index(word1)] = oppositeList[wordList.index(word1)]
                pair_a.append(word1)
                pair_b.append(oppositeList[wordList.index(word1)])
                oppositeSentences.append(' '.join(cell1))

        for word in wordList:
            if word in cell2:
                valid_phrase2 = True
                word2 = word

        if bool(valid_phrase2):
            if row[2] in original:
                pass
            else:
                original.append(row[2])
                cell2[cell2.index(word2)] = oppositeList[wordList.index(word2)]
                pair_a.append(word2)
                pair_b.append(oppositeList[wordList.index(word2)])
                oppositeSentences.append(' '.join(cell2))

df = pd.DataFrame()
df['Original'] = original
df['Opposite'] = oppositeSentences
df['S_a'] = pair_a
df['S_b'] = pair_b
df.to_csv(os.path.dirname(__file__) + '/opposites_sent_pairs.csv', sep=',', header=None, index=None)

print(".csv created with opposite syntactical analogies")
