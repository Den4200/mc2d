import json

import arcade

from mc2d.config import SCALING, SELECTION_BOX, TILE_SIZE
from mc2d.core import (
	Grid,
	Inventory,
	MapGenerator,
	Player,
	World
)
from mc2d.utils import Block


class Factory:

	def __init__(self, mc2d=None, map_generator=None, grid=None, inventory=None, player=None, world=None):
		self.mc2d = mc2d
		self.map_generator = map_generator
		self.grid = grid
		self.inventory = inventory
		self.player = player
		self.world = world

	def dump(self, fp):
		json.dump(self.serialize(), fp)

	def load(self, fp, menu):
		save = json.load(fp)

		self.mc2d = Mc2d(menu, **save['Mc2d'])

		self.map_generator = MapGenerator(self.mc2d, **save['MapGenerator'])

		self.grid = Grid(
			self.mc2d,
			selection=save['Grid']['selection'],
			should_not_check=save['Grid']['should_not_check']
		)

		for box_spec in save['Grid']['boxes']:
			self.grid.boxes.append(
				arcade.Sprite(**box_spec)
			)

		self.inventory = Inventory(self.mc2d)

		for idx, inv_sprite_spec in enumerate(save['Inventory']['inv_sprites']):
			self.inventory.inv_sprites.append(
				Block(**inv_sprite_spec)
			)
			self.inventory.block_amounts.append(
				arcade.draw_text(
					str(inv_sprite_spec['amount']),
					inv_sprite_spec['center_x'] + int(TILE_SIZE * SCALING) - (24 * SCALING),
					inv_sprite_spec['center_y'] - int(TILE_SIZE * SCALING) + (24 * SCALING),
					arcade.color.WHITE,
	                font_size=10 * SCALING + idx * 0.01,
	                bold=True
				)
			)

		self.inventory.selected_item = arcade.Sprite(
			**{
				spec_name: spec for spec_name, spec in save['Inventory']['selected_item'].items()
				if spec_name != 'index'
			}
		)
		self.inventory.selected_item.index = save['Inventory']['selected_item']['index']

		self.player = Player(self.mc2d, **save['Player'])
		
		self.world = World(self.mc2d)

		for block_spec in save['World']['block_list']:
			self.world.block_list.append(
				Block(**block_spec)
			)

		self.world.map_generator = self.map_generator

		self.mc2d.world = self.world
		self.mc2d.grid = self.grid
		self.mc2d.player = self.player
		self.mc2d.inventory = self.inventory

	def serialize(self):
		return {
			'Mc2d': {
				'view_bottom': self.mc2d.view_bottom,
				'view_left': self.mc2d.view_left
			},
			'MapGenerator': {
				'chunk_size_x': self.map_generator.chunk_size_x,
				'chunk_size_y': self.map_generator.chunk_size_y,
				'chunks': self.map_generator.chunks,
				'chunk_pos_x': self.map_generator.chunk_pos_x
			},
			'Grid': {
				'selection': self.grid.selection,
				'should_not_check': self.grid.should_not_check,
				'boxes': [
					{
						'filename': str(SELECTION_BOX),
						'scale': box.scale,
						'center_x': box.center_x,
						'center_y': box.center_y
					} for box in self.grid.boxes
				]
			},
			'Inventory': {
				'inv_sprites': [
					{
						'filename': inv_sprite.filename,
						'scale': inv_sprite.scale,
						'center_x': inv_sprite.center_x,
						'center_y': inv_sprite.center_y,
						'name': inv_sprite.name,
						'amount': inv_sprite.amount
					} for inv_sprite in self.inventory.inv_sprites
				],
				'selected_item': {
					'filename': str(SELECTION_BOX),
					'scale': self.inventory.selected_item.scale,
					'center_x': self.inventory.selected_item.center_x,
					'center_y': self.inventory.selected_item.center_y,
					'index': self.inventory.selected_item.index
				}
			},
			'Player': {
				'filename': self.player.filename,
				'scale': self.player.scale,
				'center_x': self.player.center_x,
				'center_y': self.player.center_y,
				'destination': self.player.destination,
				'button': self.player.button,
				'prev_coords': self.player.prev_coords,
				'just_started': self.player.just_started
			},
			'World': {
				'block_list': [
					{
						'filename': block.filename,
						'scale': block.scale,
						'center_x': block.center_x,
						'center_y': block.center_y,
						'name': block.name
					} for block in self.world.block_list
				]
			}
		}
