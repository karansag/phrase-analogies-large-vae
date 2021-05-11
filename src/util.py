import hashlib
import uuid

import pandas as pd
import torch


def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def write_tmp_file(frame):
    output_filename = "/tmp/{}.csv".format(uuid.uuid4().hex[:10])
    frame.to_csv(output_filename)
    return output_filename


def add_hash_column(frame):
    """Adds a column hashing columns a,b,c,d together in the CSV file corresponding to `filepath`"""

    def fn(_frame):
        return hashlib.sha256(
            (_frame["a"] + _frame["b"] + _frame["c"] + _frame["d"]).encode("utf-8")
        ).hexdigest()[:20]
        return

    frame["hash"] = frame.apply(fn, axis=1)
    return frame
