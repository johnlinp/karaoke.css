import os
import generator

class CssGenerator(generator.Generator):
	def generate(self):
		css_rules = []

		self._append_general(css_rules)
		self._append_beats(css_rules)

		self._write_file(css_rules)


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

		shape_boy = CssRule('.shape-boy')
		shape_boy.add_declaration('fill', '#34495e')

		shape_girl = CssRule('.shape-girl')
		shape_girl.add_declaration('fill', '#c0392b')

		shape_both = CssRule('.shape-both')
		shape_both.add_declaration('fill', '#27ae60')

		shadow = CssRule('.shadow')
		shadow.add_declaration('fill', '#000000')
		shadow.add_declaration('fill-opacity', '.4')

		shadow_show = CssRule('@keyframes shadow-show')
		shadow_show.add_keyframe(0, 0)
		shadow_show.add_keyframe(100, 0)

		css_rules.append(whole)
		css_rules.append(content)
		css_rules.append(screen)
		css_rules.append(shape_boy)
		css_rules.append(shape_girl)
		css_rules.append(shape_both)
		css_rules.append(shadow)
		css_rules.append(shadow_show)


	def _append_beats(self, css_rules):
		second_per_beat = 60.0 / self._config.beat_per_minute
		delay = self._config.begin_time
		for idx, beat in enumerate(self._config.beats):
			duration_beats = sum(beat['beats'])
			duration_seconds = second_per_beat * duration_beats

			if beat['lyric'] is None:
				delay += duration_seconds
				continue

			shadow = CssRule('.shadow-{}'.format(idx))
			shadow.add_declaration('transform', 'translateX(-1200px)')
			shadow.add_declaration('animation', 'shadow-show {}s'.format(duration_seconds))
			shadow.add_declaration('animation-delay', '{}s'.format(delay))

			shape_move = CssRule('.shape-move-{}'.format(idx))
			shape_move.add_declaration('transform', 'translateX(-1200px)')
			#shape_move.add_declaration('animation', 'lyric-run-{} 5s'.format(idx))
			#shape_move.add_declaration('animation-delay', '3s')

			#lyric_run = CssRule('@keyframes lyric-run-{}'.format(idx))
			#lyric_run.add_keyframe(0, -1100)
			#lyric_run.add_keyframe(10, -1040)
			#lyric_run.add_keyframe(15, -1040)
			#lyric_run.add_keyframe(25, -980)
			#lyric_run.add_keyframe(30, -980)
			#lyric_run.add_keyframe(35, -920)
			#lyric_run.add_keyframe(40, -920)
			#lyric_run.add_keyframe(50, -860)
			#lyric_run.add_keyframe(55, -860)
			#lyric_run.add_keyframe(65, -800)
			#lyric_run.add_keyframe(100, -800)

			css_rules.append(shadow)
			css_rules.append(shape_move)
			#css_rules.append(lyric_run)

			delay += duration_seconds


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


	def add_keyframe(self, progress, translate):
		assert self._is_keyframes
		self._keyframes.append((progress, translate))


	def to_string(self):
		rule_string = '{} {{\n'.format(self._selector)

		if not self._is_keyframes:
			for property_, value in self._declarations.items():
				rule_string += '\t{}: {};\n'.format(property_, value)
		else:
			for keyframe in self._keyframes:
				progress = keyframe[0]
				translate = keyframe[1]
				rule_string += '\t{}% {{\n'.format(progress)
				rule_string += '\t\ttransform: translateX({}px);\n'.format(translate)
				rule_string += '\t}\n'

		rule_string += '}\n\n'

		return rule_string
