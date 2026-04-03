#!/bin/bash

conda create --name unsloth_env \
    python=3.10 \
    pytorch=2.6.0 \
    pytorch-cuda=12.4 \
    cudatoolkit xformers -c pytorch -c nvidia -c xformers \
    -y
conda activate unsloth_env

pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124 --cache-dir pip_cache/ --force-reinstall
pip install xformers --cache-dir pip_cache/ --index-url https://download.pytorch.org/whl/cu124 --force-reinstall
pip install unsloth jupyterlab ipywidgets --cache-dir /network-volume/pip_cache
