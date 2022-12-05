from PIL import Image
import numpy as np
from command import Level

image = Image.open('demo.png')
level = Level(image)
