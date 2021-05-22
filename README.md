# Phrase Analogies in Large VAEs 
Research project on sentence embeddings in VAEs 

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
* Run run.py in the terminal with required arguments 

CSV files can run with path to the CSV as the only required argument. 

```
python3 run.py \...\example.csv
```

Individual analogies can run with three phrases in quotation marks as the required arguments.

```
python3 run.py "a" "b" "c"
```

The temperature of language generation can be madified with the argument -t x where x is some numerical value. (Default is set to 1)

```
python3 run.py -t 0.1 \...\example.csv
```

Additional optional arguments can be found with -h or --help

```
python3 run.py [-h|--help]
```

### Dataset format (CSV)
The expected input file should be a .csv file with columns `sent_a`, `sent_b`, `sent_c`, and `sent_d`. Newlines separate rows and commas separate columns. A header row is expected.

There must be one analogy per row in the form `sent_a:sent_b::sent_c:sent_d` (`sent_a` is to `sent_b` as `sent_c` is to `sent_d`)

The output file contains the model predicted solution `sent_d` for each analogy. Each prediction can then be compared to the original `sent_d` to determine the model's understanding of the pairs and/or its ability to find a correct transformation from the analogy.

The datasets used for this project, and the code that generated them, can be found in the dataset folder.


The expected input file should be a .csv file with columns `sent_a`, `sent_b`, `sent_c`, and `sent_d`. Newlines separate rows and commas separate columns. A header row is expected.

There must be one analogy per row in the form `sent_a:sent_b::sent_c:sent_d` (`sent_a` is to `sent_b` as `sent_c` is to `sent_d`)

The output file contains the model predicted solution `sent_d` for each analogy. Each prediction can then be compared to the original `sent_d` to determine the model's understanding of the pairs and/or its ability to find a correct transformation from the analogy.

The datasets used for this project, and the code that generated them, can be found in the dataset folder.

### Parameters
The function `run_experiment` takes a `temperature` parameter that allows you to determine the temperature of the language generation when producing a prediction for `sent_d`.
