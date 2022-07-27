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

def load_assets(asset_info):
    assets = []
    for key in asset_info:
        assets.append(prepare_file(key, asset_info[key][1]))
    return assets