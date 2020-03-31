# setup spacy nlp for coref resolution
import spacy
import neuralcoref

nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)


# download/load bert model
from keras.models import load_model
from keras_bert import get_custom_objects
import os.path
from omdena_wri.utils import download_bert

# check if bert model is already downloaded
assert os.path.isfile('omdena_wri/static/coref_bert.hdf5'), "Pretrained Bert Model Not Found at omdena_wri/static/coref_bert.hdf5. Please Download it from this url: https://drive.google.com/file/d/13fGAjaPzEZO1aIMw__uatccWJY17MoBu/view"

# load bert model
bert_model = load_model('omdena_wri/static/coref_bert.hdf5', custom_objects=get_custom_objects())


# prepare preproc for bert model the texts
import ktrain.text.preprocessor as tpp
preproc_type = tpp.TEXT_PREPROCESSORS.get('bert', None)
preproc = preproc_type(maxlen=350,
                        max_features=35000,
                        classes = ['pos','neg'],
                        lang='en', ngram_range=1)

# load other files
import pickle

# load TfidfVectorizer
with open('omdena_wri/static/vectorizer.pkl', 'rb') as fh:
	vectorizer = pickle.load(fh)

# load topic model
with open('omdena_wri/static/topic_model.pkl', 'rb') as fh:
	topic_model = pickle.load(fh)

# set topics 
import numpy as np
TOPICS = np.array(['land, resettlement, degradation', 'crops, farm, agriculture', 
'mining, coal, sand', 'forest, trees, deforestation', 'animal, attacked, tiger', 'drought, climate change, rain', 'water, drinking, dams'])

# load preprocessed tfidf of policy documents
with open('omdena_wri/static/policy_tfidfs.pkl', 'rb') as fh:
	policy_tfidfs = pickle.load(fh)


# execute document_classifier code
from omdena_wri.classifier import document_classifier



