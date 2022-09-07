import pygame

def filter_list_by_properties(orig_list, properties, property_number):
    list_section = []
    for index, item in enumerate(orig_list):
        item_properties = properties[index]
        if not item_properties[property_number]:
            list_section.append(item)
    return list_section

def draw_rect_list(parent_surface, rect_list, colour):
    for rect in rect_list:
        pygame.draw.rect(parent_surface, colour, rect)

def get_centered_coords(asset, screen_dims_half):
    object_width_half = int(asset.get_width()/2)
    object_height_half = int(asset.get_height()/2)
    return (screen_dims_half[0]-object_width_half, screen_dims_half[1]-object_height_half)

def get_hitbox(asset, coordinates):
    hitbox = pygame.Rect(coordinates, asset.get_size())
    return hitbox

def move_hitbox(orig_hitbox, map_offset, additional_offset=(0,0)):
    new_hitbox = orig_hitbox.copy()
    new_hitbox.topleft = (orig_hitbox.x + map_offset[0] + additional_offset[0], orig_hitbox.y + map_offset[1] + additional_offset[1])
    return new_hitbox