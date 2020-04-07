import pyglet
import string
import random
from glob import glob

def center_image(image):
    """Calculate position of image from its center not its lowerleft point."""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

def x_center_image(image):
    """Calculate position of image from its center not its lowerleft point."""
    image.anchor_x = image.width // 2
    return image

window = pyglet.window.Window(1024, 768)

rocket_image = center_image(pyglet.resource.image("assets/rocket.png"))

class Rocket:
    def __init__(self, letter: str, velocity: float, initial_x: int, initial_y: int):
        self.letter = letter
        self.velocity = velocity

        self.rocket_sprite = pyglet.sprite.Sprite(img=rocket_image, x=initial_x, y=initial_y)

        letter_offset_x = -7
        letter_offset_y = -20
        self.letter_label = pyglet.text.Label(font_size=24, text=letter, color=(0, 0, 0, 255), x=initial_x + letter_offset_x, y=initial_y + letter_offset_y)

    def draw(self):
        self.rocket_sprite.draw()
        self.letter_label.draw()

    def update(self, dt):
        self.rocket_sprite.y -= self.velocity * dt
        self.letter_label.y -= self.velocity * dt

    @property
    def y(self):
        return self.rocket_sprite.y - rocket_image.height // 2

    @property
    def x(self):
        return self.rocket_sprite.x

explosion_image_files = sorted(glob('assets/explosion/*'))
explosion_images = [x_center_image(pyglet.resource.image(i)) for i in explosion_image_files]
explosion_animation = pyglet.image.Animation.from_image_sequence(explosion_images, duration=0.05, loop=False)

def create_explosion(x: int):
    sprite = pyglet.sprite.Sprite(explosion_animation, x=x, y=0)
    sprite.scale = 5
    return sprite

def create_random_rocket() -> Rocket:
    max_x = 800
    min_v = 50
    max_v = 200
    x = random.randrange(0, max_x)
    v = random.randrange(min_v, max_v)
    l = random.choice(string.ascii_uppercase)
    rocket = Rocket(letter=l, velocity=v, initial_x=x, initial_y=window.height)
    return rocket

rockets = []
explosions = []
time_since_last_rocket = 0
time_to_next_rocket = 0
def update(dt):
    global time_since_last_rocket
    global time_to_next_rocket

    time_since_last_rocket += dt

    if time_since_last_rocket >= time_to_next_rocket:
        rocket = create_random_rocket()
        rockets.append(rocket)
        time_since_last_rocket = 0.0
        time_to_next_rocket = random.random()

    for rocket in [r for r in rockets]:
        rocket.update(dt)

        # check if exploded
        if rocket.y < 0:
            rockets.remove(rocket)
            explosions.append(create_explosion(rocket.x))

pyglet.clock.schedule_interval(update, 1/120.0)

@window.event
def on_draw():
    window.clear()

    for obj in rockets:
        obj.draw()

    for explosion in explosions:
        explosion.draw()

def symbol_to_char(symbol):
    return chr(symbol - 32)

@window.event
def on_key_press(symbol, modifier):
    for rocket in [r for r in rockets]:
        if symbol_to_char(symbol) == rocket.letter:
            rockets.remove(rocket)  

if __name__ == '__main__':
    pyglet.app.run()