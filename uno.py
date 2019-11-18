import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy.signal import find_peaks

# Load an image in grayscale
img = cv.imread('doremi.PNG', cv.IMREAD_GRAYSCALE)
chosen_thresh, bw = cv.threshold(img,0,1,cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
# cv.imshow('Binary', bw)
# cv.waitKey(0)
# cv.destroyAllWindows()

row_sum = np.sum(bw, axis=1)
index = np.arange(0, row_sum.size)

# plt.plot(index,row_sum) 
# plt.show()

peaks, mappa = find_peaks(row_sum, prominence = int(row_sum.size / 2))
# plt.plot(row_sum)
# plt.plot(peaks, row_sum[peaks], "x")
# plt.plot(np.zeros_like(row_sum), "--", color="gray")
# plt.show()

# print(peaks)
# print(type(peaks))
# print(peaks[0])
# print(mappa)
print(type(max(mappa['prominences']).astype(np.uint8)))
# print(bw == )

# bw[bw > (max(mappa['prominences']) / 2).astype(np.uint8)] = 0
# row_sum = np.sum(bw, axis=1)
# index = np.arange(0, row_sum.size)

# plt.plot(index,row_sum) 
# plt.show()