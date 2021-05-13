#!/usr/bin/python3
import argparse
import os, sys, io, datetime, platform
import pickle as p

import analogy as an
import experiment as e
import buckets


def main(args):
    return e.optimus_evaluate(
        args.input_path, args.output_path, n_samples=1, temperature=1.0, npartitions=16
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run evaluation on analogy data using OPTIMUS. Does NOT score."
    )
    parser.add_argument(
        "input_path", type=str, help="path to input file (includes s3 file paths)"
    )

    parser.add_argument(
        "output_path", type=str, help="path to output file (includes s3 file paths)"
    )

    args = parser.parse_args()
    main(args)
