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

## LICENSE
Copyright (c) 2022 yu9824  
Released under the GNU Lesser General Public License Version 3.

This software uses the following libraries.

pandas: https://github.com/pandas-dev/pandas  
BSD 3-Clause License  
Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData  
Development Team  
All rights reserved.  
Copyright (c) 2011-2020, Open source contributors.

numpy: https://github.com/numpy/numpy  
BSD 3-Clause License  
Copyright (c) 2005-2021, NumPy Developers.  
All rights reserved.

PySimpleGUI: https://pysimplegui.readthedocs.io/en/latest/  
GNU Lesser General Public License Version 3  
Copyright (c) 2018, 2019, 2020, PySimpleGUI.org

py2app: https://pypi.org/project/py2app  
MIT License  
Copyright (c) 2004-2006, Bob Ippolito <bob at redivi.com>.  
Copyright (c) 2010-2012, Ronald Oussoren <ronaldoussoren at mac.com>.
