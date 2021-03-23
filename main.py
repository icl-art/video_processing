import numpy as np
import cv2 as cv
import os
import glob
from stage import *
from progress.counter import Counter
# from resolution.image_super_resolution import predict
# from interpolation.interpolate import interpolate_imgs
import yaml

MSE_THRESH = 10
LEADING_ZEROS = 5
FORMAT_STRING = "{:05d}.jpeg"
MAX_FRAMES = 10**LEADING_ZEROS
DOWNSCALE = 2


def split_video(filepath: str, output_dir: str, metadata):
    files = glob.glob(filepath+'/*')
    for f in files:
        os.remove(f)

    cap = cv.VideoCapture(filepath)

    prev = None
    curr = None
    i = 0
    mse = 100
    counter = Counter("Splitting ")
    while cap.isOpened():
        ret, curr = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            break

        if prev is not None:
            mse = (np.square(curr - prev)).mean(axis=None)
        if mse > MSE_THRESH:
            new_size = (curr.shape[1]//DOWNSCALE, curr.shape[0]//DOWNSCALE)
            resized = cv.resize(curr, new_size)
            cv.imwrite(output_dir+FORMAT_STRING.format(i), resized)
        prev = curr
        i += 1
        counter.next()
    cap.release()
    yield

def upscale(input_dir: str, output_dir: str, metadata):
    files = os.listdir(input_dir)
    for filename in files:
        img = cv.imread(filename)
        cv.imwrite(output_dir+filename, predict(img))
        yield

def remove_cut(input_dir: str, output_dir: str, metadata):
    files = os.listdir(input_dir)
    prev = files[0]
    for filename in files[1:]:
        interpolate_imgs(prev, filename)
        yield

def recombine(input_dir: str, output_dir: str, metadata):
    split_files = glob.glob(input_dir+'/*.jpeg')
    print()
    img_array = []
    for filename in split_files:
        img = cv.imread(filename)
        height, width, _ = img.shape
        size = (width,height)
        img_array.append(img)
        yield

    out = cv.VideoWriter('output_dir/project.mp4',cv.VideoWriter_fourcc(*'DIVX'), 15, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


split_stage = file_stage("Split", "split/", split_video)
upscale_stage = stage("Upscale", "upscale/", upscale)
remove_cut_stage = stage("Remove Cuts", "output/", remove_cut)
recombine_stage = stage("Recombine", "video/", recombine)

name_to_stage = {
    "split": split_stage,
    "upscale": upscale_stage,
    "remove_cuts": remove_cut_stage,
    "recombine": recombine_stage
}

if __name__ == "__main__":
    with open("./config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)

    stages = [name_to_stage[i] for i in config.get("stages")]
    pipe = pipeline("input.mp4", stages)
    output_dir = pipe.execute(True, True)

