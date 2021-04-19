import csv

import funcy as f
import analogy as a


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


def run_experiment(inputs, n_samples=1, temperature=1):
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

    evaluator = f.partial(
        a.eval_analogy, vae, encoder_data["tokenizer"], decoder_data["tokenizer"]
    )
    preds = [
        map(
            lambda inp: evaluator(inp[0], inp[1], inp[2], temperature=temperature),
            inputs,
        )
        for _ in range(n_samples)
    ]
    return list(zip(*preds))


def compute_statistics(preds, outputs):
    """
    Compute statistics on the output
    """
    pass


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
            writer.writerow(inp + [get_pred_str(pred)] + [outp])


def run(input_filename, output_filename):
    inputs, outputs = read_csv(input_filename)
    preds = run_experiment(inputs)
    write_output(output_filename, "", inputs, preds, outputs)
