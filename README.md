environmental-conflict-tracker
==============================

**TODO**: @johnmbrandt: 
*  example jurisictional linkage
*  identification of typology for matching dictionaries
*  urls data folder
*  data/references folder with data/references/acled
*  data/policy folder with policy.pdf files

This project scrapes news media articles to identify environmental conflict events such as resource conflict, land appropriation, human-wildlife conflict, and supply chain conflict. With an initial focus on India, the project also aims to connect conflict events to their jurisdictional policies to identify how to mediate conflict events or to identify where there is a gap in legislation.

The data collection involves the following steps:

1.  Pulling all news data in a given country that contains a conflict event
2.  Keyword extraction of candidate articles from titles of news articles based on regular expression matches to a curated dictionary
3.  Scraping of full news media text for candidate articles with `NewsPlease`
4.  Manual curation of gold standard dataset, stored in `data/gold_standard/`

## Notebooks

*  0-quickstart: Inspect the data
*  1-download: Download GDELT data for a given country for an input period of time
*  2-scrape: Subset and scrape full text of candidate event articles
*  3-gold-standard: Create and save a gold standard dataset

## Roadmap

The project has been curated to allow participants in the Omdena challenge to tackle a wide range of data science needs. The ultimate end-goal is to generate maps of conflict events with extracted information about their `actors`, `types`, `numbers`, `actions`, `locations`, and `dates`. This extracted information should be paired with metadata about and text from policy documents to identify which policies have jurisdiction over the conflict event.

### Named entity recognition

We are interested in identifying the following entities: `actor`, `type`, `number`, `action`, `location`, `date`, which can be disaggregated as follows:

*  Actor: farmer, government, trader, smallholder, etc.
*  Type: Human-wildlife conflict, land tenure, land appropriation, land use rights, water scarcity, resource scarcity, livelihoods, 
*  Number: number of people affected
*  Action: Protest, kill, threaten, seize, etc.
*  Location - provided in the `data/metadata/variables/$MONTH.csv`
*  Date: Either listed in the article or `date_publish` from the text

The named entity recognition process will likely involve metadata extracted from GDELT in the `data/metadata/variables/$MONTH.csv` folder -- containing information about the types of conflict, the actors, the locations, and the dates. However, this extracted information is meant to be noisy and will likely be paired with a manually curated NER pipeline.

### Document classification

Although relying on NER itself may be sufficient, we expect that the data is currently too noisy and candidate articles will need to be extracted prior to performing NER. We have manually curated a small gold standard dataset, in `data/gold-standard`, that contains the `month` and `ids` of news articles that refer to an environmental conflict. These can be paired with the `data/metadata/variables` or `data/texts/$MONTH/$ID.pkl` by using the `data/metadata/matching/$MONTH` dictionary to identify the full text or metadata for each known positive example.

Although various options exist, we suggest an initial starting point would be to generate weakly supervised class labels for the other documents with Snorkel, and to then classify the documents with Snorkel's API. Documents with a probability above a threshold should be selected as candidates for NER.

### Jurisdictional policies

We are unclear as to the best methodology to tie conflict events to their jurisdictional policies and are open to suggestions or experimentation. This could be a manually defined algorithm or an NLP matching algorithm. The goal is to use the extracted information to pair a conflict event with a policy that should govern it. This will help highlight the gaps between policy and practice for use in stakeholder engagement.

### Visualization

We aim to create a simple dashboard with leaflet to visualize the geolocated conflict events.

## Getting started

1. Clone this repository
2. Unzip the files located in `data/texts/*`
3. Load the gold standard dataset and extract the full text and metadata from the articles

```python
import pickle
import pandas as pd
from newsplease import NewsPlease

def load_obj(month, idx):
    month = str(month).zfill(2)
    idx = str(idx).zfill(5)
    with open("data/texts/{}/{}.pkl".format(month, idx), "rb") as f:
        return pickle.load(f)
        
gs = pd.read_csv('../data/gold-standard/gold_standard.csv')
    
gs_articles = {}

for i in range(len(gs)):
    article = load_obj(gs['month'][i], gs['ids'][i])
    gs_articles[i] = article
```

4. Load the metadata attached to one of the gold standard articles

```python
import pickle
import pandas as pd

def load_dict(month):
    month = str(month).zfill(2)
    with open("data/metadata/matching/{}.pkl".format(month), "rb") as f:
        return pickle.load(f)

gs = pd.read_csv('../data/gold-standard/gold_standard.csv')
gs_sample = gs.iloc[1]

def match_metadata(gs_sample):
    month = str(gs_sample['month']).zfill(2)
    idx = gs_sample['ids']
    matching_dictionary = load_dict(month)
    print('This sample matches these rows in {}.csv: {}'.format(month, matching_dictionary[idx]))
    df = pd.read_csv("../data/metadata/variables/{}.csv".format(month))
    return df.iloc[matching_dictionary[idx]]
    
match_metadata(gs_sample)
```

## Organization

    |-- data
        |-- metadata
            |-- matching
                |-- month1.pkl # dictionary mapping urls to variables/month{}.csv
                |-- ...        # because GDELT may extract multiple conflict events per article
                |-- month12.pkl
            |-- variables
                |-- month1.csv # all GDELT extracted data on event
                |-- ...
                |-- month12.csv
        |-- texts
            |-- month1.zip # unzip to create a folder containing the below
                |-- 00000.pkl
                    |-- # indexed with doc.title, doc.text, doc.publish_date
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
--------
