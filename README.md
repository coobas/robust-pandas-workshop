# Robust Data Transformation with Pandas: Typing, Validation, Testing

Materials for Robust Pandas Workshop, EuroPython, Prague, 2023

## Preparation

Please prepare a Python environment that you can use during the workshop.
We will work in Jupyter Notebook as well as in an editor or an IDE of your choice.
Recommended are [Visual Studio Code](https://code.visualstudio.com) or [PyCharm](https://www.jetbrains.com/pycharm/).

### Clone this repository

```bash
git clone https://github.com/coobas/robust-pandas-workshop.git
```

or using `gh` client:

```bash
gh repo clone coobas/robust-pandas-workshop
```

### Prepare Python Environment

We have included either `requirements.txt` or `environment.yml` files for you to create a Python environment
using either `pip` or `conda` respectively.

Python version 3.10+ is required.

First, `cd` into the repository directory:

```bash
cd robust-pandas-workshop
```

#### Pip installation

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

#### Conda installation

```bash
conda env create -f environment.yml -n robust-pandas-workshop
conda activate robust-pandas-workshop
```
