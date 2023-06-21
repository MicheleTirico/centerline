# centerline

## Info

## Installation

Using [conda](https://docs.conda.io/en/latest/miniconda.html), create a new environment:

````bash
conda env create -f conda/env.yaml
````

Activate the environment:
````bash
conda activate centerline
````

install the sources:

````bash
python3 -m pip install -e .
````

Update the environment:
````bash
conda env update --name centerline --file  conda/env.yaml --prune
````

## TODO
- test import packages 
- change name of packages in import

