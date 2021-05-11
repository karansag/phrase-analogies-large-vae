#!/usr/bin/python3
import os, sys, io, datetime, platform
import analogy as an
import experiment as e
import pickle as p
import buckets


def run_csv(*args, **kwargs):
    return e.run(*args, **kwargs)


encoder = None
decoder = None
vae = None


if os.path.exists("encoder.pkl") and os.path.exists("decoder.pkl"):
    with open("encoder.pkl", "rb") as encoder_in:
        encoder = p.load(encoder_in)
    with open("decoder.pkl", "rb") as decoder_in:
        decoder = p.load(decoder_in)
    vae = an.get_vae(
        encoder["model"], decoder["model"], encoder["tokenizer"], decoder["tokenizer"]
    )


def set_vae():
    global encoder
    global decoder
    global vae
    encoder = an.get_encoder()
    decoder = an.get_decoder()
    vae = an.get_vae(
        encoder["model"], decoder["model"], encoder["tokenizer"], decoder["tokenizer"]
    )
    with open("encoder.pkl", "wb") as encoder_out:
        p.dump(encoder, encoder_out, p.HIGHEST_PROTOCOL)
    with open("decoder.pkl", "wb") as decoder_out:
        p.dump(decoder, decoder_out, p.HIGHEST_PROTOCOL)


def run_single(a, b, c, temperature=0.01):
    if encoder == None or decoder == None:
        set_vae()
        print()

    return an.eval_analogy(
        vae,
        encoder["tokenizer"],
        decoder["tokenizer"],
        a,
        b,
        c,
        temperature=temperature,
        degree_to_target=1,
    )


HELP_TEXT = """
Hi! Welcome to the cli utility to run OPTIMUS to evaluate analogies. The arguments are:
To evaluate a csv file
python3 run.py [--help|-h] [--partitions|-p <int>] [--temperature|-t <float>] [--scores|-s <comma-separated list>] [-n <num samples>] [-e <eval_csv>] [-o <output_csv>] <input_csv>
    input_csv     The csv containing the analogies you want to evaluate.
                  Should have columns a,b,c,d at the very least.
    eval_csv      OPTIONAL. The intermediate (unscored) results path.
                  Default value: <input_csv_name>_evl.csv
    output_csv    OPTIONAL. Where you want to output your results.
                  Default value: <input_csv_name>_res.csv
    --scores,-s   OPTIONAL. Comma-separated list of scores you want to evaluate for
                  Possible values are: nli, bleu, exact
                  Example usage: -s bleu,exact
                  Default value: (bleu, exact)
    -n            OPTIONAL. Number of samples to evaluate from the dataset
                  More samples == longer runtime

    Note that, if you have s3 credentials set up for boto3 and a bucket called 'optimus-experiments',
    the CSV arguments accept s3 paths of the form 's3://<s3 file path>'
To evaluate a single analogy
python3 run.py [--help|-h] [--temperature|-t <float>] <a> <b> <c>
    a,b,c         Three sentences which correspond to the analogy form
                  a:b::c:d where d is the sentence you are evaluating for
                  Be sure to wrap each sentence like, '"<my sentence>"'
Global parameters
    --help,-h         OPTIONAL. Show this message.
    --temperature,-t  OPTIONAL. Temperature at which to evaluate the analogies
                      Default value: 1
    --reset, -r       OPTIONAL. Removes the saved encoder and decoder
"""

# method that is run when the file is run
def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        return print(HELP_TEXT)

    is_csv = False

    npartitions = 8
    if "--partitions" in sys.argv or "-p" in sys.argv:
        idx = [
            x
            for x in range(len(sys.argv))
            if sys.argv[x] == "--partitions" or sys.argv[x] == "-p"
        ][0] + 1
        npartitions = int(sys.argv[idx])
        print("Running on {} partitions.".format(npartitions))
        del sys.argv[idx - 1 : idx + 1]

    temp = 1
    if "--temperature" in sys.argv or "-t" in sys.argv:
        idx = [
            x
            for x in range(len(sys.argv))
            if sys.argv[x] == "--temperature" or sys.argv[x] == "-t"
        ][0] + 1
        temp = float(sys.argv[idx])
        print("Evaluating with temperature: {}".format(temp))
        del sys.argv[idx - 1 : idx + 1]

    scores = ("nli", "bleu")
    if "--scores" in sys.argv or "-s" in sys.argv:
        is_csv = True
        idx = [
            x
            for x in range(len(sys.argv))
            if sys.argv[x] == "--scores" or sys.argv[x] == "-s"
        ][0] + 1
        scores = tuple(sys.argv[idx].split(","))
        print("Evaluating scores: {}".format(scores))
        del sys.argv[idx - 1 : idx + 1]

    num_samples = 1
    if "-n" in sys.argv:
        is_csv = True
        idx = [x for x in range(len(sys.argv)) if sys.argv[x] == "-n"][0] + 1
        num_samples = int(sys.argv[idx])
        print("Evaluating with num_samples: {}".format(num_samples))
        del sys.argv[idx - 1 : idx + 1]

    eval_file = ""
    if "-e" in sys.argv:
        is_csv = True
        idx = [x for x in range(len(sys.argv)) if sys.argv[x] == "-e"][0] + 1
        output_file = sys.argv[idx]
        print("Saving intermediate results to file: {}".format(output_file))
        del sys.argv[idx - 1 : idx + 1]

    output_file = ""
    if "-o" in sys.argv:
        is_csv = True
        idx = [x for x in range(len(sys.argv)) if sys.argv[x] == "-o"][0] + 1
        output_file = sys.argv[idx]
        print("Saving to file: {}".format(output_file))
        del sys.argv[idx - 1 : idx + 1]

    if "--reset" in sys.argv or "-r" in sys.argv:
        if os.path.exists("encoder.pkl") or os.path.exists("decoder.pkl"):
            os.remove("encoder.pkl")
            os.remove("decoder.pkl")
            return print("Encoder and Decoder have been reset")
        else:
            return print("No Encoder or Decoder currently exists")
        idx = [
            x
            for x in range(len(sys.argv))
            if sys.argv[x] == "-r" or sys.argv[x] == "--reset"
        ][0] + 1
        del sys.argv[idx - 1 : idx + 1]

    if len(sys.argv) <= 1:
        raise Exception("No input data was provided")

    if not is_csv and os.path.isfile(sys.argv[1]):
        is_csv = True

    if not is_csv and len(sys.argv) <= 3:
        raise Exception("Expected sentences to calculate analogy but recieved none")

    if is_csv:
        file_path = (
            sys.argv[1]
            if buckets.is_remote_file(sys.argv[1])
            else os.path.realpath(sys.argv[1])
        )

        eval_path = (
            eval_file
            if buckets.is_remote_file(eval_file) or len(eval_file) > 0
            else file_path[:-4] + "_eval.csv"
        )

        output_file = (
            output_file
            if buckets.is_remote_file(output_file) or len(output_file) > 0
            else file_path[:-4] + "_results.csv"
        )

        return run_csv(
            file_path,
            eval_path,
            output_file,
            n_samples=num_samples,
            scores=scores,
            temperature=temp,
            npartitions=npartitions,
        )
    else:
        a, b, c = sys.argv[1:]
        return run_single(a, b, c, temperature=temp)


if __name__ == "__main__":
    main()
