import pygame
import os
import alterAsset
pygame.mixer.init()

def get_filepath(file_name, is_picture):
    if is_picture:
        return os.path.join("Assets", "Sprite-" + file_name + ".png")
    else:
        return os.path.join("Assets", file_name + ".mp3")

def prepare_file(file_name, is_picture=True, scale_factor=1):
    if is_picture:
        asset = pygame.image.load(get_filepath(file_name, is_picture))
        asset = alterAsset.resize_asset(asset, scale_factor)
        return asset
    else:
        file = pygame.mixer.music.load(get_filepath(file_name, is_picture))
        return file

def get_hitbox(asset, coordinates):
    hitbox = pygame.Rect(coordinates, asset.get_size())
    return hitbox

def get_asset_properties(file_info):
    asset_properties = []
    for key in file_info:
        file_properties = file_info[key]
        for coord_set in file_properties[1]:
            file_properties_list = list(file_properties).copy()
            file_properties_list[1] = coord_set
            asset_properties.append(file_properties_list)
    print(asset_properties)
    return asset_properties

def load_resources(file_info):
    assets, hitboxes, sound_files = [], [], []
    for key in file_info:
        file_properties = file_info[key]
        if file_properties[0]:
            for coord_set in file_properties[1]:
                asset = prepare_file(key, True, file_properties[2])
                assets.append(asset)
                hitboxes.append(get_hitbox(asset, coord_set))
        else:
            asset = prepare_file(key, False)
            sound_files.append(asset)
    return assets, hitboxes, sound_files