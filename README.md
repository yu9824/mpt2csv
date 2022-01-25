# mpt2csv

## Installation
### Create a new virtual conda environment
```bash
conda create -yn mpt2csv python==3.9.6 --file requirements-conda.txt
```

### Activate the environment
```
conda activate mpt2csv
```

### Install by using pypi
```
pip install -r requirements-pip.txt
```

To sum it all up;
```
conda create -yn mpt2csv python==3.9.6 --file requirements-conda.txt && conda activate mpt2csv && pip install -r requirements-pip.txt
```

If you want to remove the environment, you can do this command;
```
conda deactivate mpt2csv    # if you need
conda remove -n mpt2csv --all
```