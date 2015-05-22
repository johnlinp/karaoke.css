import os
import generator

class HtmlGenerator(generator.Generator):
	def generate(self):
		html_dom = self._grow_html_tree()
		self._write_file(html_dom)


	def _grow_html_tree(self):
		html = HtmlDom('html')
		html.append_child(self._grow_head_tree())
		html.append_child(self._grow_body_tree())
		return html


	def _grow_head_tree(self):
		head = HtmlDom('head')

		title = HtmlDom('title')
		title.append_child(self._config.song_name)

		meta = HtmlDom('meta')
		meta.set_attr('charset', 'utf8')

		link = HtmlDom('link')
		link.set_attr('rel', 'stylesheet')
		link.set_attr('href', 'css/karaoke.css')

		head.append_child(title)
		head.append_child(meta)
		head.append_child(link)

		return head


	def _grow_body_tree(self):
		body = HtmlDom('body')

		content = HtmlDom('div')
		content.set_attr('class', 'content')

		screen = HtmlDom('svg')
		screen.set_attr('class', 'screen')

		position = 'left'
		for idx, beat in enumerate(self._config.beats):
			if beat['lyric'] is None:
				position = 'left'
				continue

			clippath = self._grow_clippath_tree(idx, beat, position)
			shape = self._grow_block_tree(idx, 'shape')
			shadow = self._grow_block_tree(idx, 'shadow')

			if position == 'left':
				position = 'right'
			elif position == 'right':
				position = 'left'
			else:
				assert False

			screen.append_child(clippath)
			screen.append_child(shape)
			screen.append_child(shadow)

		content.append_child(screen)

		body.append_child(content)

		return body


	def _grow_clippath_tree(self, idx, beat, position):
		clippath = HtmlDom('clippath')
		clippath.set_attr('id', 'lyric-{}'.format(idx))

		text = HtmlDom('text')
		text.append_child(beat['lyric'])
		if position == 'left':
			text.set_attr('text-anchor', 'start')
			text.set_attr('x', '100px')
			text.set_attr('y', '80%')
		elif position == 'right':
			text.set_attr('text-anchor', 'end')
			text.set_attr('x', '1100px')
			text.set_attr('y', '90%')
		else:
			assert False

		clippath.append_child(text)

		return clippath


	def _grow_block_tree(self, idx, which):
		block = HtmlDom('g')
		block.set_attr('clip-path', 'url(#lyric-{})'.format(idx))

		rect = HtmlDom('rect')
		rect.set_attr('width', '100%')
		rect.set_attr('height', '100%')

		if which == 'shape':
			rect.set_attr('class', 'shape-move-{} shape-boy'.format(idx))
		elif which == 'shadow':
			rect.set_attr('class', 'shadow shadow-{}'.format(idx))
		else:
			assert False

		block.append_child(rect)

		return block


	def _write_file(self, html_dom):
		self._make_sure_output_dir()
		filename = os.path.join(self._config.output_dir_name, 'index.html')
		with open(filename, 'w') as file_:
			file_.write(self._html5_doctype())
			file_.write(html_dom.to_string())


	def _html5_doctype(self):
		return '<!doctype html>\n'


class HtmlDom(object):
	def __init__(self, tag_name):
		self._tag_name = tag_name
		self._attrs = {}
		self._children = []


	def set_attr(self, attr_name, attr_value):
		self._attrs[attr_name] = attr_value


	def append_child(self, child):
		self._children.append(child)


	def to_string(self, level=0):
		attrs_string = ['{}="{}"'.format(name, value) for name, value in self._attrs.items()]
		attrs_string = ' '.join(attrs_string)
		if attrs_string:
			attrs_string = ' ' + attrs_string

		dom_string = '{}<{}{}>\n'.format('\t' * level, self._tag_name, attrs_string)

		for child in self._children:
			if isinstance(child, str):
				dom_string += '{}{}\n'.format('\t' * (level + 1), child)
			elif isinstance(child, HtmlDom):
				dom_string += child.to_string(level + 1)
			else:
				raise Exception('Unsupported html dom child type: {}'.format(type(child)))

		dom_string += '{}</{}>\n'.format('\t' * level, self._tag_name)

		return dom_string
