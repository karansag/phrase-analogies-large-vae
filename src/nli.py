import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from .util import get_device


def eval_nli(model, a_values, b_values):
    """Evaluate the NLI relationship (entailment, negative, neutral) between these pairs"""
    index_to_label = {0: "contradiction", 1: "neutral", 2: "entailment"}
    device = get_device()
    nli_model = AutoModelForSequenceClassification.from_pretrained(
        "joeddav/xlm-roberta-large-xnli"
    )
    tokenizer = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli")

    preds = []
    for a, b in zip(a_values, b_values):
        x = tokenizer.encode(
            a, b, return_tensors="pt", truncation_strategy="only_first"
        )
        logits = nli_model(x.to(device))[0]
        logit_argmax = torch.argmax(logits[:], dim=1)[1]
        preds.append(index_to_label[logit_argmax.item()])

    return preds
