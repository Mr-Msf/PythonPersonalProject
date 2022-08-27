import pygame

def get_dimensions(asset):
    return asset.get_size()

def center_rect(rect, screen_w_half, screen_h_half):
    rect.x += screen_w_half
    rect.y += screen_h_half
    return rect

def resize_asset(asset, scale_factor):
    new_lengths = (get_dimensions(asset)[0]*scale_factor, get_dimensions(asset)[1]*scale_factor)
    asset = pygame.transform.scale(asset, new_lengths)
    return asset

def rotate_asset(asset, rotation_factor):
    asset = pygame.transform.rotate(asset, rotation_factor)
    return asset

def filter_list_by_properties(orig_list, properties, property_number):
    list_section = []
    for index, item in enumerate(orig_list):
        item_properties = properties[index]
        if not item_properties[property_number]:
            list_section.append(item)
    return list_section

def move_hitbox(orig_hitbox, map_offset, additional_offset=(0,0)):
    new_hitbox = orig_hitbox.copy()
    new_hitbox.topleft = (orig_hitbox.x + map_offset[0] + additional_offset[0], orig_hitbox.y + map_offset[1] + additional_offset[1])
    return new_hitbox

def get_centered_coords(asset, screen_dims_half):
    object_width_half = int(asset.get_width()/2)
    object_height_half = int(asset.get_height()/2)
    return (screen_dims_half[0]-object_width_half, screen_dims_half[1]-object_height_half)