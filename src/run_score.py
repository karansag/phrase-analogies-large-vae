#!/usr/bin/python3
import argparse
import os, sys, io, datetime, platform
import pickle as p

import analogy as an
import experiment as e
import buckets


def main(args):
    scores = [x.strip() for x in args.scores.split(",")]
    return e.score_csv(args.input_path, args.output_path, scores=scores, n_samples=1)


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

    parser.add_argument("scores", type=str, help="The score methods to sue")

    args = parser.parse_args()
    main(args)
