import urllib.request


def download_bert():
	"""Downloads bert model trained on coref data. Size 1.2GB

		Parameters:
		None

		Returns:
		None

	"""
	print('Beginning Pretrained Bert Model download with urllib2...')
	url = 'https://doc-00-54-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/5gj50sc9l7juud57s9sh2hi3qfv19q78/1573567200000/03212935574333647640/*/13fGAjaPzEZO1aIMw__uatccWJY17MoBu?e=download'
	urllib.request.urlretrieve(url, 'omdena_wri/static/coref_bert.hdf5')

