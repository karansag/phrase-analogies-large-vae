import re
from nltk.translate import bleu_score as nltkbleu
from typing import List, Optional

import nli


def bleu_calc(output, pred):
    try:
        assert isinstance(output, str) and isinstance(pred, str)
    except AssertionError:
        print("Error: Trying to compare {} and {}".format(output, pred))
        return 0
    min_length = min(len(pred.split(" ")), len(output.split(" ")), 4)
    return bleu_compute(pred, [output], k=min_length)


def exact_calc(output, pred):
    try:
        assert isinstance(output, str) and isinstance(pred, str)
    except AssertionError:
        print("Error: Trying to compare {} and {}".format(output, pred))
        return 0
    return int(output.lower() == pred.lower())


def nli_calc(sent_c, predicted_d):
    """
    sent_c is a list /tensor / series of c sentences, predicted_d a list/tensor/series of predicated d sentences.
    Returns one of entailment/contradiction/neutral for each value in the series
    """
    return nli.eval_nli(sent_c, predicted_d)


# Following adapted from
# https://github.com/facebookresearch/ParlAI/blob/2426d74b93184689be5067bdbf99f1ba96748f7b/parlai/core/metrics.py


re_art = re.compile(r"\b(a|an|the)\b")
re_punc = re.compile(r'[!"#$%&()*+,-./:;<=>?@\[\]\\^`{|}~_\']')


def normalize_answer(s):
    """
    Lower text and remove punctuation, articles and extra whitespace.
    """

    s = s.lower()
    s = re_punc.sub(" ", s)
    s = re_art.sub(" ", s)
    # TODO: this could almost certainly be faster with a regex \s+ -> ' '
    s = " ".join(s.split())
    return s


def bleu_compute(guess: str, answers: List[str], k: int = 4) -> float:
    """
    Compute approximate BLEU score between guess and a set of answers.
    """
    # Warning: BLEU calculation *should* include proper tokenization and
    # punctuation etc. We're using the normalize_answer for everything though,
    # so we're over-estimating our BLEU scores.  Also note that NLTK's bleu is
    # going to be slower than fairseq's (which is written in C), but fairseq's
    # requires that everything be in arrays of ints (i.e. as tensors). NLTK's
    # works with strings, which is better suited for this module.
    weights = [1 / k for _ in range(k)]
    score = nltkbleu.sentence_bleu(
        [normalize_answer(a).split(" ") for a in answers],
        normalize_answer(guess).split(" "),
        smoothing_function=nltkbleu.SmoothingFunction(epsilon=1e-12).method1,
        weights=weights,
    )
    return score
