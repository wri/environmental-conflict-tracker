# omdena_wri
This package combines following tasks 

1) Apply Coref Resolution to the text

2) Use BERT trained on coref data to predict if given text is positive or negetive (pos=land/env conflict related; it'll require 1.2gb download)

3) Topic Modeling for finding relevant topics

4) Policy matching using cosine similarity

## How to Use

First of all download this [pretrained bert model](https://drive.google.com/file/d/13fGAjaPzEZO1aIMw__uatccWJY17MoBu/view) from google drive, rename it to coref_bert.hdf5 and place it in the static directory.

Check out this [Demo Notebook](demo_omdena_wri.ipynb) for quick overview.

```
>>> from omdena_wri import document_classifier
>>> document_classifier(text) # Returns tuple of bool (indicating if land conflict), array of matched topics, matched policy and cosine similarity score.
```

```
Returns tuple of bool (indicating if land conflict), array of matched topics, matched policy and cosine similarity score.

	Parameters:
		text (str): news article as a string object

	Returns:
		is_conflict (bool): True if text is an env/land conflict; false otherwise.
		topics (ndarray): List of matched topics, empty array if not a conflict
		matched_policy: Name of matched policy document, empty string if no match
		cosine_similarity_score: similarity score of text and matched policy
```

# Requirements
- spacy==2.1.0
- python -m spacy download en
- neuralcoref
- ktrain
- stellargraph
- corextopic
