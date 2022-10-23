import pygame, time, asset_creator

class Switch():
    def __init__(self, asset, connected_door_asset_indices):
        self.asset = asset
        self.saved_time = time.time()
        self.connected_door_asset_indices = connected_door_asset_indices
        self.position = True
        self.update()

    def update(self):
        if self.position:
            self.asset.rotate(self.asset.orig_rotation+30)
        else:
            self.asset.rotate(self.asset.orig_rotation-30)

    def flip(self, other_hitbox, door_assets):
        if self.asset.check_collision(other_hitbox) and self.saved_time + 0.3 < time.time():
            self.position = not self.position
            self.saved_time = time.time()
            self.move_doors(door_assets)
            self.update()

    def move_doors(self, door_assets):
        for asset_index in self.connected_door_asset_indices:
            door_assets[asset_index].state = not door_assets[asset_index].state

class Door:
    def __init__(self, asset, default_state):
        self.asset = asset
        self.state = default_state

    def reverse(self):
        if self.state:
            self.asset.orig_hitbox.topleft = (1000000,1000000)
        else:
            self.asset.orig_hitbox.topleft = self.asset.orig_coords

class Projectile:
    def __init__(self, asset, movement_per_frame, dmg_amount=500):
        self.asset = asset
        self.movement_per_frame = movement_per_frame
        self.dmg_amount = dmg_amount

    def update_position(self):
        self.asset.move(self.movement_per_frame)
    
    def reset_position(self):
        self.asset.asset_offset = (0,0)

    def check_all_collision(self, hitboxes):
        colliding = False
        for hitbox in hitboxes:
            if self.asset.check_collision(hitbox):
                colliding = True
        return colliding

class Word:
    def __init__(self, asset, trigger_rect=pygame.Rect(0,0,0,0)):
        self.asset = asset
        self.map_offset = [0,0]
        self.trigger_rect = asset_creator.Hitbox(trigger_rect, True)
        self.is_visible = False
        self.saved_time = time.time()
        self.permanently_non_visible = False
        self.update(self.map_offset)

    def update(self, map_offset):    
        if self.is_visible and self.permanently_non_visible == False:
            self.asset.orig_hitbox.topleft = self.asset.orig_coords
        else:
            self.saved_time = time.time()
            self.asset.orig_hitbox.topleft = (1000000,1000000)
        
        if time.time() - self.saved_time >= 6:
            
            self.permanently_non_visible = True
        self.trigger_rect.update_position(map_offset)

    def check_collision(self, detection_hitbox):
        if self.trigger_rect.orig_hitbox != pygame.Rect(0,0,0,0):
            if self.trigger_rect.check_collision(detection_hitbox):
                self.is_visible = True