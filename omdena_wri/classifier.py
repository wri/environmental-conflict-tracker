from . import bert_model, preproc
from omdena_wri.preprocessing import coref
from omdena_wri.modeling import topic_modeling, policy_match


def is_land_conflict(text):
	"""Returns True if text is environmental conflict related, otherwise returns False
		
		Parameters:
		text (str): news article as a string object

		Returns:
		is_conflict (bool): True if text is an env/land conflict; false otherwise.

	"""

	# preprocess the text
	(text_processed,  _) = preproc.preprocess_train([text], verbose=1)

	# return model's prediction 
	return bool(bert_model.predict(text_processed).argmax(axis=1) )


def document_classifier(text):
	'''Returns tuple of bool (indicating if land conflict), array 
	of matched topics, matched policy and cosine similarity score.

		Parameters:
		text (str): news article as a string object

		Returns:
		is_conflict (bool): True if text is an env/land conflict; false otherwise.
		topics (ndarray): List of matched topics, empty array if not a conflict
		matched_policy: Name of matched policy document, empty string if no match
		cosine_similarity_score: similarity score of text and matched policy

	'''

	# coref resolution
	text = coref(text)

	# predict if land conflict related
	if not is_land_conflict(text):
		# not land related conflict, return
		return False, {}, '', 0

	# topic modeling
	topics = topic_modeling(text)

	# policy match using cosine similarity
	if len(topics) > 0:
		matched_policy, cosine_similarity_score = policy_match(text)
	else:
		# not land related conflict, return
		return False, {}, '', 0

	return True, topics, matched_policy, cosine_similarity_score

