#**************************************************#
#    THIS FILE USES THE OFFICIAL RIFE LIBRARY.     #
# FOUND AT HTTPS://GITHUB.COM/HZWER/ARXIV2020-RIFE #
#**************************************************#

import os
import glob
import math


model_path = os.path.dirname(__file__)+"\\models"
output_path = "output"

if not os.path.exists(output_path):
    os.mkdir(output_path)

#Interpolates between 2 images, and saves the results at output_dir
#Automatically renames the generated files
#For example if:
# img1 = 0001.jpg
# img2 = 0004.jpg
# then it will create 2 frames (0002.jpg, 0003.jpg)
def interpolate_imgs(img1, img2):
    #Parse img1 to get base number
    start = _get_num(img1)
    end = _get_num(img2)
    dirname = os.path.dirname(img1)
    n_leading_zeros = len(start)
    first = int(start)+1
    n = int(end) - first
    if n == 0:
        return
    level = int(math.log2(n))

    #Generate results
    cmd = f"python {model_path}\\inference_img.py --img {img1} {img2} --exp={level}"
    os.system(cmd)

    files = glob.glob(output_path+"\\*")
    to_move = files[1:-1]
    f_string = dirname+r"/{:0%dd}.jpeg" % n_leading_zeros
    for f in to_move:
        os.rename(f, f_string.format(first))
        first += 1

    # Clear results
    os.remove(files[0])
    os.remove(files[-1])

def _get_num(filepath):
    return os.path.basename(filepath).split(".")[0]

    