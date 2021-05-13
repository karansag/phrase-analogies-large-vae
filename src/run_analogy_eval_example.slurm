#!/bin/bash
#SBATCH --job-name=analogy-eval
#SBATCH --open-mode=append
#SBATCH --output=/home/${USER}/%j_%x.out
#SBATCH --error=/home/${USER}/%j_%x.err
#SBATCH --export=ALL
#SBATCH --time=48:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=64G
#SBATCH -c 4

singularity exec --overlay $SCRATCH/overlay-25GB-500K.ext3:ro /scratch/work/public/singularity/cuda10.1-cudnn7-devel-ubuntu18.04-20201207.sif /bin/bash -c "
source /ext3/env.sh
conda activate
OPTIMUS_CHECKPOINT_DIR=/scratch/${USER}/phrase-analogies-large-vae/pretrained_models/optimus_beta10_size768-snli/checkpoint-31250 python3 run.py -s bleu,exact ../datasets/comparative_sample_large.csv
"
