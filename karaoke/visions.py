# -*- coding: utf8 -*-

import re
import os
from xml.dom import minidom
import generator

class VisionsGenerator(generator.Generator):
	def generate(self):
		self._make_sure_output_dir()
		self._make_sure_output_dir('visions')

		for vision in self._config.visions:
			if vision['name'] is None:
				continue

			basename = '{}.svg'.format(vision['name'])
			src_filename = os.path.join(self._config.visions_dir_name, basename)
			dst_filename = os.path.join(self._config.output_dir_name, 'visions', basename)
			self._generate_clip_paths(src_filename, dst_filename)


	def _generate_clip_paths(self, src_filename, dst_filename):
		document = minidom.parse(src_filename)
		self._rename_clip_paths(document)
		self._ungroup_clip_paths(document)
		self._dump_clip_paths(dst_filename, document)


	def _rename_clip_paths(self, document):
		# clipPath id -> layer name
		mapping = {}

		groups = document.getElementsByTagName('g')
		for group in groups:
			layer_name = group.getAttribute('inkscape:label')
			if not layer_name: # not a layer
				continue
			clip_path_id = self._get_clip_path_id(group)
			mapping[clip_path_id] = layer_name

		for clip_path_id, layer_name in mapping.items():
			clip_path = self._get_clip_path_by_id(clip_path_id, document)
			clip_path.setAttribute('id', layer_name)


	def _ungroup_clip_paths(self, document):
		clip_paths = document.getElementsByTagName('clipPath')

		for clip_path in clip_paths:
			non_groups = self._get_non_groups(clip_path)
			self._clear_children(clip_path)
			self._fill_children(clip_path, non_groups)


	def _get_clip_path_id(self, layer):
		children = layer.getElementsByTagName('*')
		first_child = children[0]

		clip_path_url = first_child.getAttribute('clip-path')
		match = re.match(r'url\(#(.*)\)', clip_path_url)
		clip_path_id = match.group(1)

		return clip_path_id


	def _get_clip_path_by_id(self, id_, document):
		clip_paths = document.getElementsByTagName('clipPath')
		for clip_path in clip_paths:
			if clip_path.getAttribute('id') == id_:
				return clip_path
		return None


	def _get_non_groups(self, dom):
		non_groups = []
		childrens = dom.getElementsByTagName('*')
		for child in childrens:
			if child.tagName != 'g':
				non_groups.append(child)
		return non_groups


	def _clear_children(self, dom):
		while dom.firstChild:
			dom.removeChild(dom.firstChild)


	def _fill_children(self, dom, children):
		for child in children:
			dom.appendChild(child)


	def _dump_clip_paths(self, dst_filename, document):
		with open(dst_filename, 'w') as writer:
			writer.write(document.toxml())

