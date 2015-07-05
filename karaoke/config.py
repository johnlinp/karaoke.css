import re

class Config(object):
	def __init__(self, filename):
		with open(filename, 'r') as file_:
			lines = file_.readlines()

		lines = self._remove_line_feed(lines)
		lines = self._remove_comment(lines)
		lines = self._remove_blank_lines(lines)

		basic, beats, visions = self._split_parts(lines)

		self._read_basics(basic)
		self._read_beats(beats)
		self._read_visions(visions)
		self._validate()


	def _remove_line_feed(self, lines):
		return [re.sub(r'\n', '', line) for line in lines]


	def _remove_comment(self, lines):
		return [re.sub(r'#.*', '', line) for line in lines]


	def _remove_blank_lines(self, lines):
		return [line for line in lines if line]


	def _split_parts(self, lines):
		basic, beats, visions = [], [], []

		target = basic
		for line in lines:
			if line.startswith('='):
				if target is basic:
					target = beats
				elif target is beats:
					target = visions
				continue

			target.append(line)

		return basic, beats, visions


	def _read_basics(self, basic):
		for line in basic:
			key, value = self._parse_key_value(line)
			setattr(self, key, value)


	def _read_beats(self, beats):
		self.beats = []

		position = 'left'
		for line in beats:
			lyric, beats = self._parse_labeld_beats(line)
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


	def _read_visions(self, visions):
		self.visions = []

		for line in visions:
			is_main_vision = not self._is_sub_vision(line)
			if is_main_vision:
				name, beats = self._parse_labeld_beats(line)
				curr = {
					'name': name,
					'beat': beats[0],
					'components': [],
				}
				self.visions.append(curr)
			else:
				color, id_ = self._parse_sub_vision(line)
				curr['components'].append({'color': color, 'id': id_})


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


	def _parse_labeld_beats(self, line):
		match = re.match(r'^\s*(\S+)\s*(.*?)\s*$', line)
		if not match:
			raise Exception('Invalid config beats format: {}'.format(line))

		lyric = match.group(1)
		if self._is_meta_label(lyric):
			lyric = None

		beats = match.group(2)
		beats = beats.split(',')
		beats = [beat.strip() for beat in beats]
		beats = [float(beat) for beat in beats]

		return lyric, beats


	def _parse_sub_vision(self, line):
		match = re.match(r'^\s*-\s*(\S+)\s*(\S+)\s*$', line)
		if not match:
			raise Exception('Invalid config beats format: {}'.format(line))
		color = match.group(1)
		id_ = match.group(2)
		return color, id_


	def _is_meta_label(self, label):
		return label.startswith('[') and label.endswith(']')


	def _is_sub_vision(self, line):
		return line.startswith('-')


	def _get_settings_types(self):
		return {
			'song_name': str,
			'lyric_writer': str,
			'melody_writer': str,
			'audio_filename': str,
			'output_dir_name': str,
			'visions_dir_name': str,
			'beat_per_minute': float,
			'begin_time': float,
			'beats': list,
		}


