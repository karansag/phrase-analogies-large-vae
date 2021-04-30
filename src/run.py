#!/usr/bin/python3
import os, sys, io, datetime, platform
import analogy as an
import experiment as e
import pickle as p


def run_csv(
    input_filename,
    output_filename,
    n_samples=1,
    scores=("bleu", "exact"),
    temperature=1,
):

    return e.run(
        input_filename,
        output_filename,
        n_samples=n_samples,
        scores=scores,
        temperature=temperature,
    )


encoder = None
decoder = None
vae = None


if os.path.exists('encoder.pkl') and os.path.exists('decoder.pkl'):
	with open('encoder.pkl', 'rb') as encoder_in:
		encoder = p.load(encoder_in)
	with open('decoder.pkl', 'rb') as decoder_in:
		decoder = p.load(decoder_in)
	vae = an.get_vae(
        encoder["model"], decoder["model"], encoder["tokenizer"], decoder["tokenizer"])
	
def set_vae():
    global encoder
    global decoder
    global vae
    encoder = an.get_encoder()
    decoder = an.get_decoder()
    vae = an.get_vae(encoder["model"], decoder["model"], encoder["tokenizer"], decoder["tokenizer"])
    with open('encoder.pkl', 'wb') as encoder_out:
    	p.dump(encoder, encoder_out, p.HIGHEST_PROTOCOL)
    with open('decoder.pkl', 'wb') as decoder_out:
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
python3 run.py [--help|-h] [--temperature|-t <float>] [--scores|-s <comma-separated list>] [-n <num samples>] [-o <output_csv>] <input_csv>
    input_csv     The csv containing the analogies you want to evaluate.
                  Should have columns a,b,c,d at the very least.
    output_csv    OPTIONAL. Where you want to output your results.
                  Default value: <input_csv_name>_res.csv
    --scores,-s   OPTIONAL. Comma-separated list of scores you want to evaluate for
                  Possible values are: nli, bleu, exact
                  Example usage: -s bleu,exact
                  Default value: (blue, exact)
    -n            OPTIONAL. Number of samples to evaluate from the dataset
                  More samples == longer runtime
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

    output_file = ""
    if "-o" in sys.argv:
        is_csv = True
        idx = [x for x in range(len(sys.argv)) if sys.argv[x] == "-o"][0] + 1
        output_file = sys.argv[idx]
        print("Saving to file: {}".format(output_file))
        del sys.argv[idx - 1 : idx + 1]
        
    if "--reset" in sys.argv or "-r" in sys.argv:
    	if os.path.exists('encoder.pkl') or os.path.exists('decoder.pkl'):
    		os.remove('encoder.pkl')
    		os.remove('decoder.pkl')
    		return print("Encoder and Decoder have been reset")
    	else:
    		return print("No Encoder or Decoder currently exists")
    	

    if len(sys.argv) <= 1:
        raise Exception("No input data was provided")

    if not is_csv and os.path.isfile(sys.argv[1]):
        is_csv = True

    if not is_csv and len(sys.argv) <= 3:
        raise Exception("Expected sentences to calculate analogy but recieved none")

    if is_csv:
        file_path = os.path.realpath(sys.argv[1])

        output_file = (
            output_file if len(output_file) > 0 else file_path[:-4] + "_results.csv"
        )

        return run_csv(
            file_path,
            output_file,
            n_samples=num_samples,
            scores=scores,
            temperature=temp,
        )
    else:
        a, b, c = sys.argv[1:]
        return run_single(a, b, c, temperature=temp)


if __name__ == "__main__":
    main()
