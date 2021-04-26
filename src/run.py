import analogy
import experiment


def run_csv(input_filename, output_filename, n_samples=1):

    return experiment.run(input_filename, output_filename, n_samples=n_samples)


encoder = None
decoder = None
vae = None


def set_vae():
    global encoder
    global decoder
    global vae
    encoder = analogy.get_encoder()
    decoder = analogy.get_decoder()
    vae = analogy.get_vae(
        encoder["model"], decoder["model"], encoder["tokenizer"], decoder["tokenizer"]
    )


def run_single(a, b, c, temperature=0.01):
    if encoder == None or decoder == None:
        set_vae()
        print()

    return analogy.eval_analogy(
        vae,
        encoder["tokenizer"],
        decoder["tokenizer"],
        a,
        b,
        c,
        temperature=temperature,
        degree_to_target=1,
    )
