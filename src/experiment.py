import csv


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


def run_experiment(inputs, n_samples=1):
    """
    Runs experiment given inputs.

    Takes `n_samples` samples from the VAE
    """
    pass


def compute_statistics(preds, outputs):
    """
    Compute statistics on the output
    """
    pass


def write_output(output_filename, summary_filename, inputs, preds, outputs):
    """
    Writes experiment results to files
    `output_filename` for the per-trial inputs, outputs, and predictions
    `summary_filename` for the summary statistics
    """
    pass
