# mpt2csv
This is only for **Mac OSX**.
## For user
You can download the latest version of this app from the [release](https://github.com/yu9824/mpt2csv/releases) page.

## For developer
### Create a new virtual conda environment
```bash
conda create -yn mpt2csv python==3.9.6 --file requirements-conda.txt
```

### Activate the environment
```
conda activate mpt2csv
```

### Install pypi package
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