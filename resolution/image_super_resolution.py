"""
This file is based off this project: https://github.com/idealo/image-super-resolution#installation

Since we don't have direct video upscaling, we convert a video into a list of images, and predict each one,
then merge them back into a video
"""

import numpy as np
from PIL import Image
from ISR.models import RDN, RRDN
import sys
sys.path.append('..')

#Set model - One of [noise-cancel, gans, psnr-small, psnr-large]
model_name = "noise-cancel"
model = RDN(weights=model_name)

def split_video(filepath: str):
    ...

# import cv2
# vidcap = cv2.VideoCapture('input.avi')
# success,image = vidcap.read()
# count = 0
# while success:
#     cv2.imwrite("output/frame%d.jpg" % count, image)     # save frame as JPEG file      
#     success,image = vidcap.read()
#     print('Read a new frame: ', success)
#     count += 1


def predict(img):
    sr_img = model.predict(np.array(img))
    return Image.fromarray(sr_img)

image = Image.open("./input/frame0.jpg")
output = predict(image)
output.save("frame0.jpg")

def stitch_video(savepath: str):
    ...