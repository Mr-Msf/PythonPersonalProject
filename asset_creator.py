import pygame
import constants, file_preparer, alterAsset

class Asset:
    def __init__(self, asset_name, coords, size_mult, other_properties):
        self.name = asset_name
        self.coords = coords
        self.size_mult = size_mult
        self.is_movable, self.is_permeable = other_properties
        self.orig_image = file_preparer.prepare_file(asset_name)
        self.image, self.rotated_image, self.resized_image = self.orig_image.copy(), self.orig_image.copy(), self.orig_image.copy()
        self.resize(size_mult)
        self.orig_hitbox = file_preparer.get_hitbox(self.image, coords)
        self.hitbox = self.orig_hitbox.copy()
        self.detectable_hitbox = pygame.Rect(0,0,0,0)
        
    def resize(self, scale_factor):
        new_side_lengths = (self.rotated_image.get_width()*scale_factor, self.rotated_image.get_height()*scale_factor)
        self.image = pygame.transform.scale(self.rotated_image, new_side_lengths)
        self.resized_image = self.image.copy()

    def rotate(self, rotation_factor):
        self.image = pygame.transform.rotate(self.resized_image, rotation_factor)
        self.hitbox.size = self.image.get_size()
        self.rotated_image = self.image.copy()

    def update_position(self, map_offset):
        self.centered_coords = alterAsset.get_centered_coords(self.image, (constants.WIDTH_HALF, constants.HEIGHT_HALF))
        if self.is_movable:
            screen_offset = map_offset
        else:
            screen_offset = (0,0)
        self.hitbox = alterAsset.move_hitbox(self.orig_hitbox, screen_offset, self.centered_coords)
        if not self.is_permeable:
            self.detectable_hitbox = self.hitbox

    def blit(self, parent_surface):
        parent_surface.blit(self.image, self.hitbox)