import pygame

def get_dimensions(asset):
    return asset.get_size()

def resize_asset(asset, scale_factor):
    new_lengths = (get_dimensions(asset)[0]*scale_factor, get_dimensions(asset)[1]*scale_factor)
    asset = pygame.transform.scale(asset, new_lengths)
    return asset

def rotate_asset(asset, rotation_factor):
    asset = pygame.transform.rotate(asset, rotation_factor)
    return asset