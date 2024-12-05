from src.classes import GameObject


class Vehicle(GameObject):
    def _init_(self, x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity, is_static, driver):
        super()._init_(x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity, is_static)
        self._driver = driver
        
    @property
    def driver(self):
        return self._driver
    
    @driver.setter
    def driver(self, new_driver):
        self._driver = new_driver
        
    def update(self, movement):
        super().update()
        self.apply_movement(movement)