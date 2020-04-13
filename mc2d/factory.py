import json

from mc2d.config import SELECTION_BOX


class Factory:

	def __init__(self, mc2d, map_generator, grid, inventory, player, world):
		self.mc2d = mc2d
		self.map_generator = map_generator
		self.grid = grid
		self.inventory = inventory
		self.player = player
		self.world = world

	def dump(self, fp):
		json.dump(self.serialize(), fp)

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
