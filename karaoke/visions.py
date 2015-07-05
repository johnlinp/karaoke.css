# -*- coding: utf8 -*-

import os
import shutil
import generator

class VisionsGenerator(generator.Generator):
	def generate(self):
		self._make_sure_output_dir()
		self._make_sure_output_dir('visions')

		for vision in self._config.visions:
			if vision['name'] is None:
				continue

			src_filename = os.path.join(self._config.visions_dir_name, '{}.svg'.format(vision['name']))
			dst_dirname = os.path.join(self._config.output_dir_name, 'visions')
			shutil.copy(src_filename, dst_dirname)

