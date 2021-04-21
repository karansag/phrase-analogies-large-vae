import re
from nltk.translate import bleu_score as nltkbleu
from typing import List, Optional


def bleu_calc(output, pred):
    output_l = output.split(" ")
    output_p = output.split(" ")
    return bleu_compute(pred, [output], k=2)


def exact_calc(output, pred):
    return int(output == pred)


def nli_calc(output, pred):
    pass


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