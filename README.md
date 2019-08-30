environmental-conflict-tracker
==============================

Scrape news media articles to identify environmental conflict events such as resource conflict, land appropriation, human-wildlife conflict, and supply chain conflict.

This pipeline involves the following steps:

1.  Pulling all news data in a given country that contains a conflict event
2.  Keyword extraction of candidate articles from titles of news articles based on regular expression matches to a curated dictionary
3.  Scraping of full news media text for candidate articles with `NewsPlease`
4.  Using gold standard dataset to be stored in `data/processed/$MONTH/$NAME.txt` to generate a classifier
5.  Generating maps of conflict events with GDELT geolocation and leaflet

## Notebooks

*  1-download: Download GDELT data for a given country for an input period of time
*  2-scrape: Subset and scrape full text of candidate event articles
*  3-gold-standard: Create and save a gold standard dataset

## Organization

    |-- data
        |-- metadata
            |-- matching
                |-- month1.pkl # dictionary mapping urls to variables/month{}.csv
                |-- ...        # because GDELT may extract multiple conflict events per article
                |-- month12.pkl
            |-- variables
                |-- month1.csv all GDELT extracted data on event
                |-- ...
                |-- month12.csv
        |-- texts
            |-- month1
                |-- 00000.pkl
                    |-- doc.title, doc.text, doc.publish_date
                |-- ...
                |-- 0000n.pkl
            |-- month2
            |-- ...
            |-- month12
        |-- urls
            |-- month1.txt # generated with set(df[url])
            |-- ...
            |-- month12.txt
        |-- gold-standard # contains hand labeled positive class examples
            |-- gold_standard.csv
                   |-- month, url, id, class

## Python scripts

*  scrape.py: `python3 scrape.py --month $MONTH` will subset and scrape a month of data, optionally with `--multiprocessing True` will parallelize the process.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md
    ├── data
    │   ├── external       <- Data from third party sources
    │   ├── interim        <- Intermediate data that has been transformed
    │   ├── processed      <- The final, canonical data sets for modeling
    │   └── raw            <- The original, immutable data dump
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, and model summaries
    │
    ├── notebooks          <- Jupyter notebooks
    │   └── event-identification
    │   └── patterns-themes
    │   └── actors-organizations
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------
