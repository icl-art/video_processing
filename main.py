import numpy as np
import cv2 as cv
import os
import glob
from resolution.image_super_resolution import predict
from interpolation.interpolate import interpolate_imgs
from progress.bar import Bar
from progress.counter import Counter
import timeit

MSE_THRESH = 10
LEADING_ZEROS = 5
FORMAT_STRING = "{:05d}.jpeg"
MAX_FRAMES = 10**LEADING_ZEROS
DOWNSCALE = 2


def split_video(filepath: str):
    files = glob.glob('split/*')
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
            cv.imwrite("split/"+FORMAT_STRING.format(i), resized)
        prev = curr
        i += 1
        counter.next()
    cap.release()

if __name__ == "__main__":
    start = timeit.default_timer()
    #Split video and downscale images
    split_video("TreesIn.mp4")
    
    split_files = os.listdir("split")
    #Upscale images
    print()
    upscaling = Bar("Upscaling ", max=len(split_files))
    for filename in split_files:
        img = cv.imread("split/"+filename)
        cv.imwrite("split/"+filename, predict(img))
        upscaling.next()

    #Interpolate dropped frames
    prev = split_files[0]
    print()
    interpolating = Bar("Interpolating ", max=len(split_files)-1)
    for filename in split_files[1:]:
        interpolate_imgs("split/"+prev, "split/"+filename)
        interpolating.next()
    
    #Recombine into video
    split_files = glob.glob('split/*.jpeg')
    print()
    recombining = Bar("Recombining ", max=len(split_files))
    img_array = []
    for filename in split_files:
        img = cv.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        recombining.next()


    out = cv.VideoWriter('project.mp4',cv.VideoWriter_fourcc(*'DIVX'), 15, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    end = timeit.default_timer()
    print(end-start)