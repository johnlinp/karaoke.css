import os

class Generator(object):
	def __init__(self, config):
		self._config = config

	def _make_sure_output_dir(self):
		if not os.path.exists(self._config.output_dir_name):
			os.mkdir(self._config.output_dir_name)

	def generate(self):
		pass
