#!/bin/bash
#SBATCH --mail-user=ks6335@nyu.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=optimus-analogy-eval
#SBATCH --open-mode=append
#SBATCH --output=/scratch/ks6335/logs-project/%j_%x.out
#SBATCH --error=/scratch/ks6335/logs-project/%j_%x.err
#SBATCH --export=ALL
#SBATCH --time=48:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=64G
#SBATCH -c 12

singularity exec --nv --overlay $SCRATCH/overlay-25GB-500K.ext3:rw /scratch/work/public/singularity/cuda10.1-cudnn7-devel-ubuntu18.04-20201207.sif /bin/bash -c "
source /ext3/env.sh
conda activate
      OPTIMUS_CHECKPOINT_DIR=/scratch/ks6335/phrase-analogies-large-vae/pretrained_models/optimus_beta10_size768-snli/checkpoint-31250 python3 run_eval.py s3://inputs/syntactic/plurals_data_10000.csv s3://optimus_evaluated/syntactic/plurals_data_10000_eval.csv
      OPTIMUS_CHECKPOINT_DIR=/scratch/ks6335/phrase-analogies-large-vae/pretrained_models/optimus_beta10_size768-snli/checkpoint-31250 python3 run_eval.py s3://inputs/syntactic/comparative_data_10000.csv s3://optimus_evaluated/syntactic/comparative_data_10000_eval.csv
"
