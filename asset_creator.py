import pygame
import constants, file_preparer, alterAsset

class Asset:
    def __init__(self, asset_name, orig_coords, other_properties, init_size_mult=1, init_rotation=0):
        self.name = asset_name
        self.orig_coords = orig_coords
        self.size_mult = init_size_mult
        self.rotation = init_rotation
        self.is_movable, self.is_permeable, self.is_collectable = other_properties
        self.orig_image = file_preparer.prepare_file(asset_name)
        self.image = self.orig_image.copy()
        self.orig_hitbox = file_preparer.get_hitbox(self.image, orig_coords)
        self.hitbox = self.orig_hitbox.copy()
        self.detectable_hitbox = pygame.Rect(0,0,0,0)
        self.status_var = False
        self.determine_type()
        self.update_image()
        
    def determine_type(self):
        if "Switch" in self.name:
            self.is_swich = True
        else:
            self.is_switch = False
        if "Door" in self.name:
            self.is_door = True
        else:
            self.is_door = False
    
    def resize(self, scale_factor):
        self.size_mult = scale_factor
        self.update_image()

    def rotate(self, rotation_factor):
        self.rotation = rotation_factor
        self.update_image()

    def update_image(self):
        new_side_lengths = (self.orig_image.get_width()*self.size_mult, self.orig_image.get_height()*self.size_mult)
        self.image = pygame.transform.scale(self.orig_image, new_side_lengths)
        self.image = pygame.transform.rotate(self.image, self.rotation)

    def update_position(self, map_offset):
        self.centered_coords = alterAsset.get_centered_coords(self.image, (constants.WIDTH_HALF, constants.HEIGHT_HALF))
        if self.is_movable:
            screen_offset = map_offset
        else:
            screen_offset = (0,0)
        self.hitbox = alterAsset.move_hitbox(self.orig_hitbox, screen_offset, self.centered_coords)
        self.hitbox.size = self.image.get_size()
        if not self.is_permeable:
            self.detectable_hitbox = self.hitbox

    def check_collision(self, other_hitbox):
        if self.hitbox.colliderect(other_hitbox):
            return True
        return False

    def blit(self, parent_surface):
        parent_surface.blit(self.image, self.hitbox)