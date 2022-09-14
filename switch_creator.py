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

    def update(self):
        if self.state:
            self.asset.orig_hitbox.topleft = (1000000,1000000)
        else:
            self.asset.orig_hitbox.topleft = self.asset.orig_coords

class Projectile:
    pass