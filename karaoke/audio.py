# -*- coding: utf8 -*-

import os
import shutil
import generator

class AudioGenerator(generator.Generator):
	def generate(self):
		self._make_sure_output_dir()
		self._make_sure_output_dir('audio')

		src_filename = self._config.audio_filename
		dst_dirname = os.path.join(self._config.output_dir_name, 'audio')
		shutil.copy(src_filename, dst_dirname)

