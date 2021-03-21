# import numpy as np
# import cv2 as cv
# import os
# import glob
# from resolution.image_super_resolution import predict

# MSE_THRESH = 10
# LEADING_ZEROS = 5
# FORMAT_STRING = "{:05d}.jpeg"
# MAX_FRAMES = 10**LEADING_ZEROS
# DOWNSCALE = 2


# def split_video(filepath: str):
#     files = glob.glob('output/*')
#     for f in files:
#         os.remove(f)

#     cap = cv.VideoCapture(filepath)

#     prev = None
#     curr = None
#     i = 0
#     mse = 100
#     while cap.isOpened():
#         ret, curr = cap.read()
#         # if frame is read correctly ret is True
#         if not ret:
#             break

#         if prev is not None:
#             mse = (np.square(curr - prev)).mean(axis=None)
#         if mse > MSE_THRESH:
#             new_size = (curr.shape[1]//DOWNSCALE, curr.shape[0]//DOWNSCALE)
#             resized = cv.resize(curr, new_size)
#             cv.imwrite("output/"+FORMAT_STRING.format(i), resized)
#         prev = curr
#         i += 1
#     cap.release()

# if __name__ == "__main__":
#     split_video("TreesIn.mp4")
#     image = cv.imread("output/00000.jpeg")
#     cv.imwrite("frame0.jpg", predict(image))

from interpolation.interpolate import interpolate_imgs

interpolate_imgs("split/00424.jpeg", "split/00429.jpeg")