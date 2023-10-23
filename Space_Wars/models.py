from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import load_sprite, load_sound, wrap_position, get_random_velocity

up = Vector2(0,-1)

class gameObject():
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width()/2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_pos = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_pos)

    def motion(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)
    
    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

class spaceShip(gameObject):
    MANEUVERABILITY = 15 #amount of rotation at once
    ACCELERATION = 5
    BULLET_SPEED = 3
    def __init__(self, position, create_callback):
        self.create_bullet_callback = create_callback
        self.laser_sound = load_sound("laser")
        self.direction = Vector2(up) 
        #a copy of vector up that acts as temporary variable for storing the required direction
        super().__init__(position, load_sprite("ship1",True), Vector2(0))

    def accelerate(self, deaccelerate=False):
        if deaccelerate == False:
            self.velocity += self.direction * self.ACCELERATION
        else:
            self.velocity -= self.direction * self.ACCELERATION

    def rotate(self, clockwise=True, stop=False):
        if stop == False :
            sign = 1 if clockwise else -1
            angle = (self.MANEUVERABILITY * sign)*self.ACCELERATION
            self.direction.rotate_ip(angle)
        # elif stop == True :
        #     sign = 0
        #     angle = self.MANEUVERABILITY * sign
        #     self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(up)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()


class Asteroid(gameObject):
    def __init__(self, position):

        super().__init__(position, load_sprite("asteroid",True), get_random_velocity(1,3))

class Bullet(gameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("laser_bullet"), velocity)

    def motion(self, surface):
        self.position = self.position + self.velocity