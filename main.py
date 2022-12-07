from PIL import Image
from command import Level

image = Image.open('demo.png')

level = Level(image)
while True:
    level.tick()
    level.create_image(20).show()