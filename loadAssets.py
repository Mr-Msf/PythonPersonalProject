import pygame
import os
import alterAsset

def get_filepath(asset_name, is_picture):
    if is_picture:
        return os.path.join("Assets", "Sprite-" + asset_name + ".png")
    else:
        pass

def prepare_file(asset_name, scale_factor=1, is_picture=True):
    if is_picture:
        asset = pygame.image.load(get_filepath(asset_name, is_picture))
        asset = alterAsset.resize_asset(asset, scale_factor)
        return asset
    else:
        pass

def get_hitbox(asset, coordinates):
    hitbox = pygame.Rect(coordinates, asset.get_size())
    return hitbox

def load_resources(asset_info):
    assets, hitboxes = [], []
    for key in asset_info:
        properties = asset_info[key]
        asset = prepare_file(key, properties[1])
        assets.append(asset)
        hitboxes.append(get_hitbox(asset, properties[0]))
    return assets, hitboxes