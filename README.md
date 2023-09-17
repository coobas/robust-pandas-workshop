# Robust Data Transformation with Pandas: Typing, Validation, Testing

Materials for [Robust Pandas Tutorial, EuroPython, Prague, 2023](https://program.europython.eu/europython-2023/talk/AEAPDB/).

## Abstract

We will explore possibilities for making our data analyses and transformations in Pandas robust and production ready. We will see how advanced group-by, resample or rolling aggregations work on large time series weather data. (As a bonus, you will learn about Prague climate.) We will use type annotations and schema validations with the Pandera library to make our code more readable and robust. We will also show the potential of property-based testing using the Hypothesis package, with strategies generated from Pandera schemas. We will show how to avoid issues with time zones when working with time series data. By the end of the tutorial, you will have a deeper understanding of advanced Pandas aggregations and be able to write robust, production ready Pandas code.

## Data sources

Two data sources are used in this workshop:
* [Open Meteo API](https://open-meteo.com/en/docs)
* [Czech Hydro-Meteorological Institute (CHMI)](https://www.chmi.cz/historicka-data/pocasi/denni-data/data-ze-stanic-site-RBCN)

## Preparation

Please prepare a Python environment that you can use during the workshop.
We will work in Jupyter Notebook as well as in an editor or an IDE of your choice.
Recommended are [Visual Studio Code](https://code.visualstudio.com) or [PyCharm](https://www.jetbrains.com/pycharm/).

*Note:* All the instructions below are for Unix-like systems (Linux, macOS, WSL on Windows).
If you want / need to work in Windows native `cmd` or PowerShell, you will need to adapt the commands accordingly.
We cannot provide support for Windows native environments.

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
conda env create -f environment.yml -n "robust-pandas-workshop"
conda activate robust-pandas-workshop
```

#### The `weatherlyser` package

Code for this workshop is in the `weatherlyser` package in this repository.
Before working with it, either in Jupyter notebooks, in your IDE, or when running tests,
Python needs to know about it.

Either set the `PYTHONPATH` environment variable to the repository directory:

```bash
export PYTHONPATH=$PWD
```
(this of course assumes your current directory in the repository root)

or, which is more robust, install the package in editable mode:

```bash
pip install -e .
```

## Online option

[Clone in Deepnote](https://deepnote.com/launch?url=https%3A%2F%2Fgithub.com%2Fcoobas%2Frobust-pandas-workshop)

Follow the instructions therein and if you do not have it, create a free Deepnote account.

## Workshop materials

All materials that we will use during the workshop are in Jupyter notebooks.

1. [Introduction](01_introduction.ipynb)
2. [First data exploration](02_first_data_exploration.ipynb)
3. [Type annotations and dataframe models](03_type_annotations.ipynb)
4. [Data loading](04_data_loading_module.ipynb)
5. [Time zones](05_time_zones.ipynb)
6. [Hypothesis testing](06_hypothesis_testing.ipynb)
7. [Grouping, resampling and aggregations](07_resampling_and_aggregations.ipynb)
8. [Windowing and differences](08_windowing_and_differences.ipynb)

Visual Studio Code or PyCharm Professional users can work with notebooks directly in their IDE;
this is the recommended way. You can also use Jupyter Lab, which will be installed in your environment
and features an IDE environment too with and editor and command line.

## Testing and linting

The `tests` directory contains tests for the `weatherlyser` package.
We will use the tests throughout the workshop to test our code.
It is also a good idea to run the tests to check whether your installation is working correctly.

To run tests, use `pytest`:
```bash
pytest
```

The `mypy` static type checker is configured to check the `weatherlyser` and `tests` folders.
You can run it with:
```bash
mypy
```
