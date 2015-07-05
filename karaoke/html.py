# -*- coding: utf8 -*-

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

		self._append_title(screen)
		self._append_lyrics(screen)
		self._append_visions(screen)

		content.append_child(screen)

		body.append_child(content)

		self._append_audio(body)

		return body


	def _append_title(self, screen):
		clippath = self._grow_title_clippath_tree()
		shape = self._grow_title_block_tree()

		screen.append_child(clippath)
		screen.append_child(shape)


	def _append_lyrics(self, screen):
		for idx, beat in enumerate(self._config.beats):
			if beat['lyric'] is None:
				continue

			clippath = self._grow_lyrics_clippath_tree(idx, beat)
			shape = self._grow_lyrics_block_tree('shape', idx)
			shadow = self._grow_lyrics_block_tree('shadow', idx)

			screen.append_child(clippath)
			screen.append_child(shape)
			screen.append_child(shadow)


	def _append_visions(self, screen):
		for idx, vision in enumerate(self._config.visions):
			if vision['name'] is None:
				continue

			filename = 'visions/{}.svg'.format(vision['name'])
			for jdx, component in enumerate(vision['components']):
				shape = self._grow_visions_block_tree(filename, component)
				screen.append_child(shape)


	def _append_audio(self, body):
		audio = HtmlDom('audio')
		audio.set_attr('control')
		audio.set_attr('autoplay')

		source = HtmlDom('source')
		audio_basename = os.path.basename(self._config.audio_filename)
		source.set_attr('src', 'audio/' + audio_basename)
		source.set_attr('type', 'audio/ogg')

		audio.append_child(source)

		body.append_child(audio)


	def _grow_title_clippath_tree(self):
		clippath = HtmlDom('clippath')

		clippath.set_attr('id', 'title')

		text = HtmlDom('text')
		text.append_child(self._config.song_name)
		text.set_attr('text-anchor', 'middle')
		text.set_attr('x', '50%')
		text.set_attr('y', '40%')
		text.set_attr('class', 'song-name')

		clippath.append_child(text)

		text = HtmlDom('text')
		text.append_child('詞：{}'.format(self._config.lyric_writer))
		text.set_attr('text-anchor', 'middle')
		text.set_attr('x', '50%')
		text.set_attr('y', '50%')
		text.set_attr('class', 'credits')

		clippath.append_child(text)

		text = HtmlDom('text')
		text.append_child('曲：{}'.format(self._config.melody_writer))
		text.set_attr('text-anchor', 'middle')
		text.set_attr('x', '50%')
		text.set_attr('y', '56%')
		text.set_attr('class', 'credits')

		clippath.append_child(text)

		return clippath

	def _grow_lyrics_clippath_tree(self, idx, beat):
		clippath = HtmlDom('clippath')

		text = HtmlDom('text')
		clippath.set_attr('id', 'lyric-{}'.format(idx))
		text.append_child(beat['lyric'])
		if beat['position'] == 'left':
			text.set_attr('text-anchor', 'start')
			text.set_attr('x', '100px')
			text.set_attr('y', '80%')
		elif beat['position'] == 'right':
			text.set_attr('text-anchor', 'end')
			text.set_attr('x', '1100px')
			text.set_attr('y', '90%')
		else:
			assert False

		clippath.append_child(text)

		return clippath


	def _grow_title_block_tree(self):
		block = HtmlDom('g')
		block.set_attr('clip-path', 'url(#title)')

		rect = HtmlDom('rect')
		rect.set_attr('width', '100%')
		rect.set_attr('height', '100%')

		rect.set_attr('class', 'title shape-title')

		block.append_child(rect)

		return block


	def _grow_lyrics_block_tree(self, which, idx):
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


	def _grow_visions_block_tree(self, filename, component):
		block = HtmlDom('g')
		block.set_attr('clip-path', 'url({}#{})'.format(filename, component['id']))
		block.set_attr('transform', 'translate(0, 350)')

		rect = HtmlDom('rect')
		rect.set_attr('width', '100%')
		rect.set_attr('height', '100%')
		rect.set_attr('fill', '#{}'.format(component['color']))

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


	def set_attr(self, attr_name, attr_value=None):
		self._attrs[attr_name] = attr_value


	def append_child(self, child):
		self._children.append(child)


	def to_string(self, level=0):
		attrs_short_strings = []
		attrs_whole_string = ''
		for name, value in self._attrs.items():
			if value is not None:
				attrs_short_strings.append('{}="{}"'.format(name, value))
			else:
				attrs_short_strings.append(name)
		attrs_whole_string = ' '.join(attrs_short_strings)
		if attrs_whole_string:
			attrs_whole_string = ' ' + attrs_whole_string

		dom_string = '{}<{}{}>\n'.format('\t' * level, self._tag_name, attrs_whole_string)

		for child in self._children:
			if isinstance(child, str):
				dom_string += '{}{}\n'.format('\t' * (level + 1), child)
			elif isinstance(child, HtmlDom):
				dom_string += child.to_string(level + 1)
			else:
				raise Exception('Unsupported html dom child type: {}'.format(type(child)))

		dom_string += '{}</{}>\n'.format('\t' * level, self._tag_name)

		return dom_string
