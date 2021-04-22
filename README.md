# Phrase Analogies in Large VAEs 
Project for MLLU class

## Setup

The following steps are necessary to setup the repository on your own device

### Download Pre Trained Models

In order to download the pretrained models, you should run the following command in your terminal

```bash
./download_pretrained_models.sh
```

This command will download all models listed from [the OPTIMUS repository](https://github.com/ChunyuanLI/Optimus/blob/master/doc/optimus_finetune_language_models.md) so it may take some time to run.

The models will be saved in a folder named `/pretrained_models` where they can be unzipped and used within your code

### Submodules
This repo uses git submodules. Please `git submodule init` and `git submodule update` the submodule found in `./Optimus`. See [https://git-scm.com/book/en/v2/Git-Tools-Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) for more information.

## Running experiments

* Change the value of `OUTPUT_DIR` in `src/analogy.py` to correspond to the directory of your model data. E.g., `OUTPUT_DIR = os.path.abspath("../../data/snli-b1/checkpoint-31250/")`
* Call the function `run` in `src/experiment.py` with your input and output filenames. For information about the input format, see below.

You can run individual analogies with `eval_analogy` in `analogy.py`

### Expected CSV format
We expect input to have columns 'sent_a', 'sent_b', 'sent_c', and 'sent_d'. A header row is expected. Newlines separate rows and commas separate columns.

The analogy is of the form `sent_a:sent_b::sent_c:sent_d`, with `sent_d` predicted by the model. This predicted `sent_d` is compared against our gold label from the input.

### Parameters
The function `run_experiment` takes a `temperature` parameter that allows you to determine the temperature of the language generation when producing a prediction for `sent_d`.
