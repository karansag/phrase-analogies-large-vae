from functools import lru_cache
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from util import get_device


@lru_cache(maxsize=None)
def get_nli_model():
    return AutoModelForSequenceClassification.from_pretrained(
        "joeddav/xlm-roberta-large-xnli"
    )


@lru_cache(maxsize=None)
def get_nli_tokenizer():
    return AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli")


def eval_nli(a_values, b_values):
    """Evaluate the NLI relationship (entailment, negative, neutral) between these pairs"""
    index_to_label = {0: "contradiction", 1: "neutral", 2: "entailment"}
    device = get_device()
    nli_model = get_nli_model()
    tokenizer = get_nli_tokenizer()
    preds = []
    for a, b in zip(a_values, b_values):
        x = tokenizer.encode(
            a, b, return_tensors="pt", truncation_strategy="only_first"
        )
        logits = nli_model(x.to(device)).logits
        logit_argmax = torch.argmax(logits[:], dim=1)[0]
        preds.append(index_to_label[logit_argmax.item()])

    return preds
