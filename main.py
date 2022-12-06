from PIL import Image
import numpy as np
from command import Level
from pprint import pprint

image = Image.open('demo.png')
level = Level(image)
pprint(vars(level))