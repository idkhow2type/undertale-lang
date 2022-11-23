from PIL import Image
import numpy as np
import command as cmd

image = Image.open('demo.png')
# print(np.asarray(image))
level = cmd.Level(image)
