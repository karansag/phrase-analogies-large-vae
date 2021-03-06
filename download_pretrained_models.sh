#!/bin/bash

if [ ! -d pretrained_models ] ; then
  mkdir pretrained_models
fi

echo "Downloading pretrained models..."
echo "This might take some time."
echo ""

# echo "Downloading pretrained model with beta=0, latent size=32"
# wget https://textae.blob.core.windows.net/optimus/output/pretrain/philly_rr3_vc4_g8_base_vae_wikipedia_pretraining_beta_schedule_beta0.0_d1.0_ro0.5_ra0.25_32_v2/checkpoint-508523.zip -O pretrained_models/optimus_beta00_size32.zip -q --show-progress
# unzip pretrained_models/optimus_beta00_size32.zip -d pretrained_models/optimus_beta00_size32

# echo ""
# echo "Downloading pretrained model with beta=0.5, latent size=32"
# wget https://textae.blob.core.windows.net/optimus/output/pretrain/philly_rr3_vc4_g8_base_vae_wikipedia_pretraining_beta_schedule_beta0.5_d1.0_ro0.5_ra0.25_32_v2/checkpoint-508523.zip -O pretrained_models/optimus_beta05_size32.zip  -q --show-progress
# unzip pretrained_models/optimus_beta05_size32.zip -d pretrained_models/optimus_beta05_size32

# echo ""
# echo "Downloading pretrained model with beta=0, latent size=768"
# wget https://textae.blob.core.windows.net/optimus/output/pretrain/philly_rr3_vc4_g8_base_vae_wikipedia_pretraining_beta_schedule_beta0.0_d1.0_ro0.5_ra0.25_768_v2/checkpoint-508523.zip -O pretrained_models/optimus_beta00_size768.zip -q --show-progress
# unzip pretrained_models/optimus_beta00_size768.zip -d pretrained_models/optimus_beta00_size768

# echo ""
# echo "Downloading pretrained model with beta=0.5, latent size=768"
# wget https://textae.blob.core.windows.net/optimus/output/pretrain/philly_rr3_vc4_g8_base_vae_wikipedia_pretraining_beta_schedule_beta0.5_d1.0_ro0.5_ra0.25_768_v2/checkpoint-508523.zip -O pretrained_models/optimus_beta05_size768.zip -q --show-progress
# unzip pretrained_models/optimus_beta05_size768.zip -d pretrained_models/optimus_beta05_size768

# echo ""
# echo "Downloading pretrained model with beta=1, latent size=768"
# wget https://textae.blob.core.windows.net/optimus/output/pretrain/philly_rr3_vc4_g8_base_vae_wikipedia_pretraining_beta_schedule_beta1.0_d1.0_ro0.5_ra0.25_768_v2/checkpoint-508523.zip -O pretrained_models/optimus_beta10_size768.zip -q --show-progress
# unzip pretrained_models/optimus_beta10_size768.zip -d pretrained_models/optimus_beta10_size768

echo ""
echo "Downloading pretrained model with beta=1, latent size=768, SNLI"
wget https://textae.blob.core.windows.net/optimus/output/LM/Snli/768/philly_vae_snli_b1.0_d5_r00.5_ra0.25_length_weighted/checkpoint-31250.zip -O pretrained_models/optimus_beta10_size768-snli.zip -q --show-progress
unzip pretrained_models/optimus_beta10_size768-snli.zip -d pretrained_models/optimus_beta10_size768-snli


echo "All done!"
