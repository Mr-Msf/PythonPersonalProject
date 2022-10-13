import pygame
import os
import constants, asset_creator, switch_creator
pygame.mixer.init()

def get_filepath(file_name, is_picture=True):
    if is_picture:
        return os.path.join("Assets", "Sprite-" + file_name + ".png")
    else:
        return os.path.join("Assets", file_name + ".mp3")

def prepare_file(file_name, is_picture=True):
    if is_picture:
        asset = pygame.image.load(get_filepath(file_name, is_picture))
        return asset.copy()
    else:
        file = pygame.mixer.music.load(get_filepath(file_name, is_picture))
        return file

def get_asset_properties(all_asset_info):
    all_asset_properties = []
    for item_properties in all_asset_info:
        for coord_set in item_properties[1]:
            item_properties_list = list(item_properties).copy()
            item_properties_list[1] = coord_set
            all_asset_properties.append(item_properties_list)
    return all_asset_properties

def center_rect(rect, screen_w_half, screen_h_half):
    rect.x += screen_w_half
    rect.y += screen_h_half
    return rect

def load_assets(asset_info):
    assets = []
    all_asset_properties = get_asset_properties(asset_info)
    for item_properties in all_asset_properties:
        asset = asset_creator.Asset(*item_properties)
        assets.append(asset)
    return assets

def get_hitboxes(all_hitbox_info):
    hitboxes = []
    for hitbox_info in all_hitbox_info:
        hitbox_info[0] = center_rect(pygame.Rect(hitbox_info[0]), constants.WIDTH_HALF, constants.HEIGHT_HALF)
        hitbox = asset_creator.Hitbox(*hitbox_info)
        hitboxes.append(hitbox)
    return hitboxes

def get_switches_and_doors(assets):
    switch_assets, door_assets, projectile_assets, word_assets = [], [], [], []
    switches, doors, projectiles, words = [], [], [], []
    for asset in assets:
        if "Switch" in asset.name:
            switch_assets.append(asset)
        elif "Door" in asset.name:
            door_assets.append(asset)
        elif "Projectile" in asset.name:
            projectile_assets.append(asset)
    for switch_asset, door_indices in zip(switch_assets, constants.DOORS_PER_SWITCH):
        switches.append(switch_creator.Switch(switch_asset, door_indices))
    for door_asset, door_state in zip(door_assets, constants.STARTING_DOOR_STATES):
        doors.append(switch_creator.Door(door_asset, door_state))
    for word_asset, word_info in zip(word_assets, constants.WORD_INFO):
        words.append(switch_creator.Word(word_asset, *word_info))

        
    return switches, doors, projectiles, words