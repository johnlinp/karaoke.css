import re

class Config(object):
	def __init__(self, filename):
		with open(filename, 'r') as file_:
			lines = file_.readlines()

		lines = self._remove_line_feed(lines)
		lines = self._remove_comment(lines)
		lines = self._remove_blank_lines(lines)

		basic, beats = self._split_basic_beats(lines)

		self._read_basic_settings(basic)
		self._read_beats(beats)
		self._validate()


	def _remove_line_feed(self, lines):
		return [re.sub(r'\n', '', line) for line in lines]


	def _remove_comment(self, lines):
		return [re.sub(r'#.*', '', line) for line in lines]


	def _remove_blank_lines(self, lines):
		return [line for line in lines if line]


	def _split_basic_beats(self, lines):
		basic, beats = [], []

		meet_split = False
		for line in lines:
			if line.startswith('='):
				meet_split = True
				continue

			if not meet_split:
				basic.append(line)
			else:
				beats.append(line)

		return basic, beats


	def _read_basic_settings(self, basic):
		for line in basic:
			key, value = self._parse_key_value(line)
			setattr(self, key, value)


	def _read_beats(self, beats):
		self.beats = []
		position = 'left'
		for line in beats:
			lyric, beats = self._parse_lyric_beats(line)
			beat = {}
			beat['lyric'] = lyric
			beat['beats'] = beats
			if lyric is None:
				position = 'left'
			else:
				beat['position'] = position
				if position == 'left':
					position = 'right'
				elif position == 'right':
					position = 'left'
				else:
					assert False

			self.beats.append(beat)


	def _validate(self):
		for key, type_ in self._get_settings_types().items():
			value = getattr(self, key)
			if type(value) is not type_:
				raise Exception('Invalid config type: {} - {}'.format(key, value))


	def _parse_key_value(self, line):
		match = re.match(r'^\s*(\S+)\s*:\s*(\S+)\s*$', line)
		if not match:
			raise Exception('Invalid config basic setting format: {}'.format(line))

		key = match.group(1)
		key = re.sub('-', '_', key)

		value = match.group(2)
		value = self._get_settings_types()[key](value)

		return key, value


	def _parse_lyric_beats(self, line):
		match = re.match(r'^\s*(\S+)\s*(.*?)\s*$', line)
		if not match:
			raise Exception('Invalid config beats format: {}'.format(line))

		lyric = match.group(1)
		if lyric.startswith('[') and lyric.endswith(']'):
			lyric = None

		beats = match.group(2)
		beats = beats.split(',')
		beats = [beat.strip() for beat in beats]
		beats = [float(beat) for beat in beats]

		return lyric, beats


	def _get_settings_types(self):
		return {
			'song_name': str,
			'lyric_writer': str,
			'melody_writer': str,
			'audio_filename': str,
			'output_dir_name': str,
			'beat_per_minute': float,
			'begin_time': float,
			'beats': list,
		}


