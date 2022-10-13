import time

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
    def __init__(self, asset, ):
        self.asset = asset
        
        self.is_visible = False

    def update(self, is_visible):
        self.is_visible = is_visible
        if self.is_visible:
            self.asset.orig_hitbox.topleft = self.asset.orig_coords
        else:
            self.asset.orig_hitbox.topleft = (1000000,1000000)