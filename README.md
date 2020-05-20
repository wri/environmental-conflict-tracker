environmental-conflict-tracker
==============================

# Description

This project develops a globally relevant index of environmental conflict at a subnational scale by reading through millions of news articles every day and identifying and locating events. Environmental conflict can occur through conflicts over resources, land, wildlife, or supply chains. Currently, the database contains thousands of conflict events in India, Indonesia, and Brazil.

# Installation

TBD.

# Usage

TBD.

# Methodology

## Data - Inputs

1.  Identifying all news data in a given country that contains a conflict event from [GDELT](https://www.gdeltproject.org/)
2.  Keyword extraction of candidate articles from titles of news articles based on regular expression matches to a curated dictionary
3.  Scraping of full news media text for candidate articles with `NewsPlease`
4.  Coreference resolution and standard text preprocessing, such as stop word removal and lemmatization

The data is stored as a JSON like so:

```javascript
{ "id": "00001",
  "country": "IN",
  "url": "https://",
  "date": "MM-DD-YYYY",
  "full_text": string,
  "article_title": string,
  "number_actions": int,
  "actions": {
      1: {'latitude', 'longitude', 'action_type', "goldstein", ...},
      2: {'latitude', 'longitude', 'action_type', "goldstein", ...},
      3: {'latitude', 'longitude', 'action_type', "goldstein", ...},
          },
  }
```

## Data - Outputs

This project identifies the following entities: `actor`, `type`, `number`, `action`, `location`, `date`, which can be disaggregated as follows:

*  Actor: farmer, government, trader, smallholder, etc.
*  Type: Human-wildlife conflict, land tenure, land appropriation, land use rights, water scarcity, resource scarcity, livelihoods, 
*  Number: number of people affected
*  Action: Protest, kill, threaten, seize, etc.
*  Location - provided in the `data/metadata/variables/$MONTH.csv`
*  Date: Either listed in the article or `date_publish` from the text

The highest priority entity is the `type` of conflict. `Location` and `Date` should be provided by the GDELT metadata `data/metadata/variables`. `Action` may be provided by the GDELT metadata through the [CAMEO codebook](http://data.gdeltproject.org/documentation/CAMEO.Manual.1.1b3.pdf) but should be verified. `Number` and `Actor` are going to be difficult to identify and will likely need an implementation of coreference resolution.

## Methodology

*  [CorEx Topic model](https://arxiv.org/abs/1611.10277)
*  [RoBERTa classifier](https://arxiv.org/abs/1907.11692)
*  [Named entity recognition](https://spacy.io/api/entityrecognizer)

### Validation

The `data/reference/` folder contains validated data from [ACLED](https://www.acleddata.com) on conflict events in India during 2017. This database refers to all conflict events, not just environmental conflict, but could be used as a baseline for regional level violence, or by keyword extraction.


## Important references
*  [GDELT](https://www.gdeltproject.org)
*  [CAMEO codebook](http://data.gdeltproject.org/documentation/CAMEO.Manual.1.1b3.pdf)
*  [Land Conflict Watch](https://www.landconflictwatch.org)
*  [WRI Restoration](https://www.wri.org/our-work/project/global-restoration-initiative)
*  [Global forest watch](https://www.globalforestwatch.org)
*  [Flair NER](https://github.com/zalandoresearch/flair)
*  [SpaCy NER](https://spacy.io/api/entityrecognizer/)
*  [Coreference resolution](https://medium.com/huggingface/state-of-the-art-neural-coreference-resolution-for-chatbots-3302365dcf30)

## Organization

    |-- data
        |-- metadata
            |-- matching
                |-- month1.pkl # dictionary mapping urls to variables/month{}.csv
                |-- ...        # because GDELT may extract multiple conflict events per article
                               # this is of the form {text/url id: [metadata/variables/month.csv row IDs]}
                               # {0: [0, 1, 2, 3, 4],
                               #  1: [5, 6],
                               #  2: [7, 11],
                               #  3: [8],
                               #  4: [9, 10, 12, 13]
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
