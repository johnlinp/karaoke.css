import os
import generator

class CssGenerator(generator.Generator):
	def generate(self):
		self._set_parameters()

		css_rules = []

		self._append_general(css_rules)
		self._append_title(css_rules)
		self._append_beats(css_rules)
		self._append_visions(css_rules)

		self._write_file(css_rules)


	def _set_parameters(self):
		# appears before count down
		self._NUM_PRE_APPEAR_BEATS = 1
		# prompt count down before the singer start to sing
		self._NUM_COUNT_DOWN_BEATS = 4
		# how long will the lyric stay after it was sung
		self._NUM_STAY_BEATS = 1
		# how long the title will stay on the screen
		self._NUM_TITLE_BEATS = 8
		# the width of a character in pixel
		self._CHAR_WIDTH = 60


	def _append_general(self, css_rules):
		whole = CssRule('html, body')
		whole.add_declaration('height', '100%')
		whole.add_declaration('margin', '0')
		whole.add_declaration('overflow', 'hidden')

		content = CssRule('.content')
		content.add_declaration('height', '100%')
		content.add_declaration('font', "'Open Sans'")
		content.add_declaration('font-size', '60px')

		screen = CssRule('.screen')
		screen.add_declaration('width', '1200px')
		screen.add_declaration('height', '100%')
		screen.add_declaration('margin', '0 auto 50px')
		screen.add_declaration('display', 'block')

		title_color = CssRule('.colorful-color-title')
		title_color.add_declaration('fill', '#16a085')

		boy_color = CssRule('.colorful-color-boy')
		boy_color.add_declaration('fill', '#34495e')

		girl_color = CssRule('.colorful-color-girl')
		girl_color.add_declaration('fill', '#c0392b')

		both_color = CssRule('.colorful-color-both')
		both_color.add_declaration('fill', '#27ae60')

		shadow_color = CssRule('.shadow-color')
		shadow_color.add_declaration('fill', '#000000')
		shadow_color.add_declaration('fill-opacity', '.4')

		title_song_name = CssRule('#title-clip .song-name')
		title_song_name.add_declaration('font-size', '80px')

		title_credits = CssRule('#title-clip .credits')
		title_credits.add_declaration('font-size', '30px')

		css_rules.append(whole)
		css_rules.append(content)
		css_rules.append(screen)
		css_rules.append(title_color)
		css_rules.append(boy_color)
		css_rules.append(girl_color)
		css_rules.append(both_color)
		css_rules.append(shadow_color)
		css_rules.append(title_song_name)
		css_rules.append(title_credits)


	def _beats_to_seconds(self, num_beats):
		second_per_beat = 60.0 / self._config.beat_per_minute
		return second_per_beat * num_beats



	def _append_title(self, css_rules):
		self._append_colorful_title_timing(css_rules)
		self._append_colorful_title_progress(css_rules)


	def _append_beats(self, css_rules):
		self._append_shadow_lyrics_timing(css_rules)
		self._append_shadow_lyrics_progress(css_rules)
		self._append_colorful_lyrics_timing(css_rules)
		self._append_colorful_lyrics_progress(css_rules)


	def _append_visions(self, css_rules):
		self._append_colorful_visions_timing(css_rules)
		self._append_colorful_visions_progress(css_rules)


	def _append_colorful_title_timing(self, css_rules):
		timing = CssRule('.colorful-title-timing')

		delay_seconds = self._config.begin_time
		duration_seconds = self._beats_to_seconds(self._NUM_TITLE_BEATS)

		timing.add_declaration('transform', 'translateX(-1200px)')
		timing.add_declaration('animation', 'colorful-title-progress {}s'.format(duration_seconds))
		timing.add_declaration('animation-delay', '{}s'.format(delay_seconds))

		css_rules.append(timing)


	def _append_colorful_title_progress(self, css_rules):
		progress = CssRule('@keyframes colorful-title-progress')
		progress.add_keyframe(0, 0)
		progress.add_keyframe(80, 0)
		progress.add_keyframe(100, 1100)

		css_rules.append(progress)


	def _append_shadow_lyrics_timing(self, css_rules):
		delay_beats = 0

		all_sections = []
		cur_section = {
			'blank': {
				'lyric': None,
				'beats': [0],
			},
			'lines': [],
		}
		all_sections.append(cur_section)

		prev_beat = None
		prev_line = None
		prev_prev_line = None

		for idx, cur_beat in enumerate(self._config.beats):
			if cur_beat['lyric'] is None:
				delay_beats += cur_beat['beats'][0]
				cur_section = {
					'blank': cur_beat,
					'lines': [],
				}
				all_sections.append(cur_section)
				continue

			if len(cur_section['lines']) == 0: # first beat
				cur_line = {
					'delay': delay_beats - self._NUM_COUNT_DOWN_BEATS - self._NUM_PRE_APPEAR_BEATS,
					'duration': self._NUM_PRE_APPEAR_BEATS + self._NUM_COUNT_DOWN_BEATS + sum(cur_beat['beats']) + self._NUM_STAY_BEATS,
					'idx': idx,
				}
			elif len(cur_section['lines']) == 1: #second beat
				cur_line = {
					'delay': cur_section['lines'][0]['delay'],
					'duration': cur_section['lines'][0]['duration'] + sum(cur_beat['beats']),
					'idx': idx,
				}
			else:
				cur_line = {
					'delay': prev_prev_line['delay'] + prev_prev_line['duration'],
					'duration': sum(prev_beat['beats']) + sum(cur_beat['beats']),
					'idx': idx,
				}

			delay_beats += sum(cur_beat['beats'])

			cur_section['lines'].append(cur_line)

			prev_prev_line = prev_line
			prev_beat = cur_beat
			prev_line = cur_line

		for section in all_sections:
			for line in section['lines']:
				shadow = CssRule('.shadow-lyrics-timing-{}'.format(line['idx']))

				delay_seconds = self._config.begin_time + self._beats_to_seconds(line['delay'])
				duration_seconds = self._beats_to_seconds(line['duration'])

				shadow.add_declaration('transform', 'translateX(-1200px)')
				shadow.add_declaration('animation', 'shadow-lyrics-progress {}s'.format(duration_seconds))
				shadow.add_declaration('animation-delay', '{}s'.format(delay_seconds))

				css_rules.append(shadow)


	def _append_shadow_lyrics_progress(self, css_rules):
		shadow_lyrics_progress = CssRule('@keyframes shadow-lyrics-progress')
		shadow_lyrics_progress.add_keyframe(0, 0)
		shadow_lyrics_progress.add_keyframe(100, 0)

		css_rules.append(shadow_lyrics_progress)


	def _append_colorful_lyrics_timing(self, css_rules):
		delay_beats = 0
		for idx, beat in enumerate(self._config.beats):
			if beat['lyric'] is not None:
				timing = CssRule('.colorful-lyrics-timing-{}'.format(idx))

				delay_seconds = self._config.begin_time + self._beats_to_seconds(delay_beats)
				duration_seconds = self._beats_to_seconds(sum(beat['beats']) + self._NUM_STAY_BEATS)

				timing.add_declaration('transform', 'translateX(-1200px)')
				timing.add_declaration('animation', 'colorful-lyrics-progress-{} {}s'.format(idx, duration_seconds))
				timing.add_declaration('animation-delay', '{}s'.format(delay_seconds))

				css_rules.append(timing)

			delay_beats += sum(beat['beats'])


	def _append_colorful_lyrics_progress(self, css_rules):
		for idx, beat in enumerate(self._config.beats):
			if beat['lyric'] is None:
				continue

			percents_per_beat = 100.0 / (sum(beat['beats']) + self._NUM_STAY_BEATS)

			progress = CssRule('@keyframes colorful-lyrics-progress-{}'.format(idx))

			if beat['position'] == 'left':
				cur_translate = -1100
			elif beat['position'] == 'right':
				cur_translate = -100 - self._CHAR_WIDTH * len(beat['lyric'].decode('utf8'))
			else:
				assert False

			progress.add_keyframe(0, cur_translate)

			cur_beats = 0
			for beat_length in beat['beats']:
				cur_beats += beat_length
				cur_translate += self._CHAR_WIDTH
				progress.add_keyframe(percents_per_beat * cur_beats, cur_translate)
			progress.add_keyframe(100, cur_translate)

			css_rules.append(progress)


	def _append_colorful_visions_timing(self, css_rules):
		delay_beats = 0
		for idx, vision in enumerate(self._config.visions):
			if vision['name'] is not None:
				for jdx, component in enumerate(vision['components']):
					delay_seconds = self._config.begin_time + self._beats_to_seconds(delay_beats)
					duration_seconds = self._beats_to_seconds(vision['beat'])

					timing = CssRule('.colorful-visions-timing-{}-{}'.format(idx, jdx))
					timing.add_declaration('transform', 'translateX(-1200px)')
					timing.add_declaration('animation', 'colorful-visions-progress {}s'.format(duration_seconds))
					timing.add_declaration('animation-delay', '{}s'.format(delay_seconds))

					css_rules.append(timing)

			delay_beats += vision['beat']


	def _append_colorful_visions_progress(self, css_rules):
		progress = CssRule('@keyframes colorful-visions-progress')
		progress.add_keyframe(0, -1200)
		progress.add_keyframe(30, 0)
		progress.add_keyframe(70, 0)
		progress.add_keyframe(100, 1200)

		css_rules.append(progress)


	def _write_file(self, css_rules):
		self._make_sure_output_dir()
		self._make_sure_output_dir('css')
		filename = os.path.join(self._config.output_dir_name, 'css', 'karaoke.css')
		with open(filename, 'w') as file_:
			for css_rule in css_rules:
				file_.write(css_rule.to_string())


class CssRule(object):
	def __init__(self, selector):
		self._selector = selector
		self._is_keyframes = selector.startswith('@keyframes')
		if self._is_keyframes:
			self._keyframes = []
		else:
			self._declarations = {}


	def add_declaration(self, property_, value):
		assert not self._is_keyframes
		self._declarations[property_] = value


	def add_keyframe(self, percent, translate):
		assert self._is_keyframes
		self._keyframes.append((percent, translate))


	def to_string(self):
		rule_string = '{} {{\n'.format(self._selector)

		if not self._is_keyframes:
			for property_, value in self._declarations.items():
				rule_string += '\t{}: {};\n'.format(property_, value)
		else:
			for keyframe in self._keyframes:
				percent = keyframe[0]
				translate = keyframe[1]
				rule_string += '\t{}% {{\n'.format(percent)
				rule_string += '\t\ttransform: translateX({}px);\n'.format(translate)
				rule_string += '\t}\n'

		rule_string += '}\n\n'

		return rule_string
