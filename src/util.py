import uuid

import torch


def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def write_tmp_file(frame):
    output_filename = "/tmp/{}.csv".format(uuid.uuid4().hex[:10])
    frame.to_csv(output_filename)
    return output_filename

