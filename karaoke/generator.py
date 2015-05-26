import os

class Generator(object):
	def __init__(self, config):
		self._config = config

	def _make_sure_output_dir(self, suffix=None):
		if not os.path.exists(self._config.output_dir_name):
			os.mkdir(self._config.output_dir_name)

		if suffix:
			path_with_suffix = os.path.join(self._config.output_dir_name, suffix)
			if not os.path.exists(path_with_suffix):
				os.mkdir(path_with_suffix)

	def generate(self):
		pass
