"""
This file is based off this project: https://github.com/idealo/image-super-resolution#installation

Since we don't have direct video upscaling, we convert a video into a list of images, and predict each one,
then merge them back into a video
"""

import numpy as np
from PIL import Image
from ISR.models import RDN
import sys
sys.path.append('..')

#Set model - One of [noise-cancel, psnr-small, psnr-large]
model_name = "noise-cancel" #this seems to work the best
model = RDN(weights=model_name)


#Upscales an image 2^scale times
def predict(array, scale):
    pred = model.predict(array)
    for i in range(scale-1):
        pred = model.predict(np.array(pred))
    return pred
