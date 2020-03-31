from . import nlp


def coref(text):
	"""Returns text after Corefrerence resolution
		
		Parameters:
		text (str): news article as a string object

		Returns:
		text_coref (str): text after coref resolved

	"""
	return nlp(text)._.coref_resolved
