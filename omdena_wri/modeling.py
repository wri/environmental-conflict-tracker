from . import vectorizer, topic_model, policy_tfidfs, TOPICS
from sklearn.metrics.pairwise import cosine_similarity


def topic_modeling(text):
	"""Returns ndarray of names of matched topics

		Parameters:
		text (str): news article as a string object


		Returns: 
		topics (numpy array): List of matched topics, empty array if no match

	"""

	# calculate tfidf of text
	text_tfidf = vectorizer.transform([text])

	# match topics 
	model_output = topic_model.transform(text_tfidf).squeeze().nonzero()[0]

	# return topic names
	return TOPICS[model_output]


def policy_match(text):
	"""Returns policy matched with text, and respective cosine similarity score
		
		Parameters:
		text (str): news article as a string object

		Returns:
		matched_policy: Name of matched policy document, empty string if no match
		
	"""

	# calculate tfidf of text
	text_tfidf = vectorizer.transform([text])

	# find policy with maximum cosine similarity using tfidf 
	max_score = 0
	matched_policy = ''
	for policy in policy_tfidfs:
		score = cosine_similarity(text_tfidf, policy_tfidfs[policy]).squeeze()
		if max_score < score:
			max_score = score
			matched_policy = policy

	# return matched policy & cosine similarity score
	return matched_policy, max_score

