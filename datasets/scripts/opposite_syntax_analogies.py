
import csv
import pandas as pd

wordList = ("acceptable"
            , "aware",
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


def remove_duplicates(phrase):
    output = []
    for x in phrase:
        if x not in output:
            output.append(x)
    return output


sentences = []
oppositeSentences = []
with open('/home/joshua/Documents/snli_1.0_train.csv', newline='') as inputfile:
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
            sentences.append(row[1])
            cell1[cell1.index(word1)] = oppositeList[wordList.index(word1)]
            oppositeSentences.append(' '.join(cell1))

        for word in wordList:
            if word in cell2:
                valid_phrase2 = True
                word2 = word

        if bool(valid_phrase2):
            sentences.append(row[2])
            cell2[cell2.index(word2)] = oppositeList[wordList.index(word2)]
            oppositeSentences.append(' '.join(cell2))

df = pd.DataFrame()
df['Original'] = remove_duplicates(sentences)
df['Opposite'] = remove_duplicates(oppositeSentences)
df.to_csv('/home/joshua/Documents/Opposites_Dataset.csv', sep=',', header=None, index=None)

print(".csv created with opposite syntactical analogies")
