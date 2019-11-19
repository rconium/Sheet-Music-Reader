import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy.signal import find_peaks

def get_index(mat, limit):
    return [i for (i, val) in enumerate(mat) if val > limit]

# Load an image in grayscale
img = cv.imread('doremi.PNG', cv.IMREAD_GRAYSCALE)
chosen_thresh, bw = cv.threshold(img,0,255,cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
# cv.imshow('image', bw)
# cv.waitKey(0)
# cv.destroyAllWindows()

row_sum = np.sum(bw, axis=1)
index = np.arange(0, row_sum.size)

# plt.plot(index,row_sum) 
# plt.show()

# peaks, mappa = find_peaks(row_sum, prominence = int(row_sum.size / 2))
# row_sum[row_sum > np.max(row_sum) / 2] = 0

# get the indices where the value is greater than half of the max value
peaks = get_index(row_sum, np.max(row_sum) / 2)

bw[peaks, :] = 0
print(bw[peaks, :])
cv.imshow('image', bw)
cv.waitKey(0)
cv.destroyAllWindows()
# plt.plot(row_sum)
# plt.plot(peaks, row_sum[peaks], "x")
# plt.plot(np.zeros_like(row_sum), "--", color="gray")
# plt.show()
