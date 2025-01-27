conda env create -f conda-env.yml
conda activate nsgt-torch
pip install pysndfile
pip install torch==1.10.1+cpu torchaudio==0.10.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install tifffile[all] "numpy<=1.23"