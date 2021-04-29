import os, sys
import pandas as pd

# source: https://gist.github.com/jrivero/1085501#file-csv_splitter-py
def split(
    filehandler,
    delimiter=",",
    row_limit=10000,
    output_name_template="output_%s.csv",
    output_path=".",
    keep_headers=True,
):
    """
    Splits a CSV file into multiple pieces.

    A quick bastardization of the Python CSV library.

    Arguments:

        `row_limit`: The number of rows you want in each output file. 10,000 by default.
        `output_name_template`: A %s-style template for the numbered output files.
        `output_path`: Where to stick the output files.
        `keep_headers`: Whether or not to print the headers in each output file.

    Example usage:

        >> from csv_splitter import csv_splitter
        >> csv_splitter.split(open('/home/ben/input.csv', 'r'))

    """
    import csv

    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(output_path, output_name_template % current_piece)
    current_out_writer = csv.writer(open(current_out_path, "w"), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = next(reader)
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path, output_name_template % current_piece
            )
            current_out_writer = csv.writer(
                open(current_out_path, "w"), delimiter=delimiter
            )
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)


def random_sample(
    filename,
    output_filename="",
    row_limit=10000,
):
    """
    Samples rows from a larger csv and creates a randomized csv with some number of rows

    Arguments:
        `filename`: The name of the file to read
        `row_limit`: The number of rows you want in each output file. 10,000 by default.
        `output_filename`: Where you want to output your sampled data

    Example usage:

        >> from csv_splitter import random_sample
        >> random_sample("../datasets/processed_comparative_pairs.csv", row_limit=5000)

    """
    input_csv = pd.read_csv(filename)
    output_csv = (
        output_filename
        if len(output_filename) > 0
        else os.path.realpath(sys.argv[1])[:-4] + "_split.csv"
    )
    sampled_df = input_csv.sample(n=row_limit)
    sampled_df.to_csv(output_csv, index=False)