environmental-conflict-tracker
==============================

# Description

This project develops a globally relevant index of environmental conflict at a subnational scale by reading through millions of news articles every day and identifying and locating events. Environmental conflict can occur through conflicts over resources, land, wildlife, or supply chains. Currently, the database contains thousands of conflict events in India, Indonesia, and Brazil.

# Installation

**Note: The Docker container is not yet released, as the project is still in early stage.**

```
docker pull johnbrandtwri/environmental_conflict_tracker:latest
docker run -p 8888:8888 johnbrandtwri/environmental_conflict_tracker
```

# Usage

TBD.

# Methodology

## Data - Inputs

1.  Identify all news data in a given country that contains a conflict event from [GDELT](https://www.gdeltproject.org/)
2.  Extract candidate articles from titles of news articles based on regular expression matches to a curated dictionary
3.  Scrape full news media text for candidate articles with `NewsPlease`
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

## Data - Internal outputs

This project identifies the following entities: `actor`, `type`, `number`, `action`, `location`, `date`, which can be disaggregated as follows:

*  Actor: farmer, government, trader, smallholder, etc.
*  Type: Human-wildlife conflict, land tenure, land appropriation, land use rights, water scarcity, resource scarcity, livelihoods, 
*  Number: number of people affected
*  Action: Protest, kill, threaten, seize, etc.
*  Location - provided in the `data/metadata/variables/$MONTH.csv`
*  Date: Either listed in the article or `date_publish` from the text

The highest priority entity is the `type` of conflict. `Location` and `Date` should be provided by the GDELT metadata `data/metadata/variables`. `Action` may be provided by the GDELT metadata through the [CAMEO codebook](http://data.gdeltproject.org/documentation/CAMEO.Manual.1.1b3.pdf) but should be verified. `Number` and `Actor` are going to be difficult to identify and will likely need an implementation of coreference resolution.

## Data - External outputs

The external output is a monthly index of environmental conflict by subnational jurisdiction. The methodology for this is TBD.

## Methodology

*  **[RoBERTa classifier](https://arxiv.org/abs/1907.11692)**: Classify articles into conflict / no conflict
*  **[CorEx Topic model](https://arxiv.org/abs/1611.10277)**: For conflict articles, identify type of conflict
*  **[Named entity recognition](https://spacy.io/api/entityrecognizer)**: For conflict articles, identify actor, action, date, and location.

## Validation

TBD. 

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

TBD.
