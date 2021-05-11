import shutil

import pandas as pd

import buckets as b
import util


def hash_input(filepath, output_filepath):
    """
    Add a 'hash' column to input CSV with columns a,b,c,d, hashing those columns

    Accepts filenames locally or of the form `s3://...`
    """
    input_filepath = b.get_file(filepath) if b.is_remote_file(filepath) else filepath
    print(input_filepath)
    frame = pd.read_csv(input_filepath)
    new_frame = util.add_hash_column(frame)
    tmp_file = util.write_tmp_file(new_frame)
    if b.is_remote_file(output_filepath):
        b.put_file(tmp_file, output_filepath)
    else:
        shutil.move(tmp_file, output_filepath)
    return output_filepath
