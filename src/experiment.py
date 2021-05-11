import csv

import os
import funcy as f
import pandas as pd
import dask.dataframe as dd
import pickle as p
import shutil
import uuid

import analogy as a
import score as s
import buckets as b
import util


def read_csv(filename):
    """
    Reads a CSV of analogies with columns a,b,c,d corresponding
    to analogy a:b::c:d.

    Returns results as
    list of inputs [[a_1, b_1, c_1], [a_2, b_2, c_2],...] and
    list of outputs [d_1, d_2, ...]
    """
    inputs = []
    outputs = []
    with open(filename, newline="") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            inputs.append(row[:3])
            outputs.append(row[3])

    return inputs, outputs


def run_experiment(input_frame, n_samples=1, temperature=1, npartitions=1):
    """
    Runs experiment given inputs.

    Takes `n_samples` samples from the VAE
    Returns a list of size `n_samples` of results for each input
    """

    encoder_data = a.get_encoder()
    decoder_data = a.get_decoder()

    vae = a.get_vae(
        encoder_data["model"],
        decoder_data["model"],
        encoder_data["tokenizer"],
        decoder_data["tokenizer"],
        beta=0,
    )
    # partially apply function for evaluator
    # series here represents a row (we call with axis=1)
    def evaluator(series):
        return a.eval_analogy(
            vae,
            encoder_data["tokenizer"],
            decoder_data["tokenizer"],
            series[0],
            series[1],
            series[2],
            temperature=temperature,
        )[0]

    new_columns = ["pred_{}".format(i) for i in range(n_samples)]
    output_frame = pd.DataFrame()
    parallelize = npartitions > 1
    for col in new_columns:
        if parallelize:
            output_frame[col] = input_frame.map_partitions(
                lambda df: df.apply(evaluator, axis=1)
            ).compute()
        else:
            output_frame[col] = input_frame.apply(evaluator, axis=1)
    return output_frame


def compute_scores(
    outputs, preds, premises=tuple(), include_scores=("bleu", "exact", "nli")
):
    """
    Compute scores on the data
    """
    results = {}
    fn_list = {"bleu": s.bleu_calc, "exact": s.exact_calc, "nli": s.nli_calc}

    for score_name in include_scores:
        fn = fn_list[score_name]
        if score_name == "nli":
            s_a, s_b, s_c, gold = premises
            nli_result_list = s.nli_calc(premises[2], preds)
            results["nli_raw"] = nli_result_list
            results["nli"] = [
                1 if x == y else 0 for (x, y) in zip(nli_result_list, gold)
            ]
        else:
            results[score_name] = list(map(lambda args: fn(*args), zip(outputs, preds)))
    return results


def get_pred_str(prediction):
    """Returns prediction string for one prediction from data returned by run_experiment"""
    return prediction[0][0]


def write_output(output_filename, summary_filename, inputs, preds, outputs):
    """
    Writes experiment results to files
    `output_filename` for the per-trial inputs, outputs, and predictions
    `summary_filename` for the summary statistics
    """
    # For now: assume only one sample
    with open(output_filename, "w", newline="") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        for inp, pred, outp in zip(inputs, preds, outputs):
            writer.writerow(inp + [get_pred_str(pred)] + [output])


def score_csv(
    input_filename_raw, output_filename, scores=("bleu", "exact"), n_samples=1
):
    input_filename = (
        b.get_file(input_filename_raw)
        if b.is_remote_file(input_filename_raw)
        else input_filename_raw
    )
    input_frame = pd.read_csv(input_filename)

    output_frame = input_frame.filter(
        [
            col
            for col in input_frame.columns
            if not col.startswith("score_") and not col.startswith("Unnamed")
        ],
        axis=1,
    )
    for i in range(n_samples):
        new_results = compute_scores(
            output_frame["d"],
            output_frame["pred_{}".format(i)],
            premises=(
                output_frame["a"],
                output_frame["b"],
                output_frame["c"],
                # The gold label category
                output_frame["category"] if "category" in output_frame else "neutral",
            ),
            include_scores=scores,
        )
        for scorer, result in new_results.items():
            output_frame["score_{num}_{scorer}".format(num=i, scorer=scorer)] = result

    if b.is_remote_file(output_filename):
        tmp_filename = util.write_tmp_file(output_frame)
        b.put_file(tmp_filename, output_filename)
    else:
        output_frame.to_csv(output_filename)
        print("Wrote output to {}".format(output_filename))
    return output_frame


def optimus_evaluate(
    input_filename, output_filepath, n_samples=1, temperature=1.0, npartitions=1
):
    """Evaluate analogies using OPTIMUS over the input"""
    experiment_id = uuid.uuid4().hex[:10]
    print("Running experiment {}".format(experiment_id))
    # Download (if necessary)
    input_filename_downloaded = (
        b.get_file(input_filename)
        if b.is_remote_file(input_filename)
        else input_filename
    )

    # Read input
    print("Read input from {}".format(input_filename_downloaded))
    input_frame = pd.read_csv(input_filename_downloaded)

    # Run optimus evaluation
    new_col_frame = run_experiment(
        dd.from_pandas(input_frame[["a", "b", "c"]], npartitions=npartitions)
        if npartitions > 1
        else input_frame[["a", "b", "c"]],
        n_samples=n_samples,
        temperature=temperature,
        npartitions=npartitions,
    )
    output_frame = pd.concat([input_frame, new_col_frame], axis=1)

    # Upload optimus evaluation
    local_filepath = util.write_tmp_file(output_frame)
    print("Writing output to {}".format(local_filepath))
    if b.is_remote_file(output_filepath):
        print("Uploading file to optimus: {}".format(output_filepath))
        b.put_file(local_filepath, output_filepath)
    else:
        print("Moving output to {}".format(output_filepath))
        shutil.move(local_filepath, output_filepath)
    return (output_frame, output_filepath)


def run(
    input_filename,
    eval_filepath,
    output_filepath,
    n_samples=1,
    scores=("bleu", "exact"),
    temperature=1,
    npartitions=1,
):
    """
    Main entry point for running experiments

    Assumes that input has columns `a`, `b`, `c`, `d` for the analogy s.t. a:b::c:d
    Uses `a` `b` `c` to make a predicted `d`.

    Takes `input_filename` for the input and an `output_filename` where it can write the output
    as CSVs

    Will run each a/b/c triplet through prediction `n_samples` times, assigning each output to a new column.

    Stores scores as column `score_{sample #}_{method #}`

    npartitions should be the number of logical cores you have (the higher this is, the faster your computation will be)

    On Ubuntu, you can get the number of cores with `grep -m 1 'cpu cores' /proc/cpuinfo`

    On mac, you can do this with `sysctl -n hw.ncpu`

    """
    (eval_frame, eval_path) = optimus_evaluate(
        input_filename,
        eval_filepath,
        n_samples=n_samples,
        temperature=temperature,
        npartitions=npartitions,
    )

    return score_csv(eval_path, output_filepath, n_samples=n_samples, scores=scores)
