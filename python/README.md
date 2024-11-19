### Develop "Python Stock-Data Analytics" Project
---

Python Environment
```
$ python --version
Python 3.9.12
```
```
$ anaconda --version
anaconda Command line client (version 1.9.0)
```
<br>

### Setting up the Python runtime environment
---
Anaconda activate.
```
conda create -n data_analytics
conda activate data_analytics
conda env list
```
<br>

Start jupyter notebook browser.
```
jupyter notebook ./jupyter/
```
<br>

Setting pandas_datareader and mplfinance.
```
pip install - U pandas_datareader mplfinance pyti kaleido
pip show pandas_datareader mplfinance pyti kaleido
```

<br>

### Install Python "TA-Lib" library
---
TA-Lib Official Documents: https://ta-lib.org/function.html

<br>

Access the following URL and download the appropriate Ta-lib for the version of Python you are using

```
$ python --version
Python 3.9.12
```
https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

<br>

ta-lib local install
```
pip install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
```
