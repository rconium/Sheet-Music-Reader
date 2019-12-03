# import the necessary packages
import numpy as np
import argparse
import imutils
import glob
import cv2
import sys
import subprocess

def open_file(path):
  cmd = {'linux':'eog', 'win32':'explorer', 'darwin':'open'}[sys.platform]
  subprocess.run([cmd, path])

# templates list
note_files = [
    "template/beam_c4_2_d4_quarter_e4_1.png",
    "template/beam_a4_1_half_b4_quarter_a4_1.png",
    "template/b3_1.png",
    "template/c4_half.png",
    "template/d4_3.png",
    "template/d4_half.png",
    "template/e4_1.png",
    "template/e4_half.png",
    "template/f4_1.png",
    "template/g4_1.png",
    "template/g4_half.png",
    "template/c5_1_half.png",
    "template/d5_1.png",]

# description of templates above
n = [
  'beam_cde4',
  'beam_aba4',
  'b3_1',
  'c4_half',
  'd4_3',
  'd4_half',
	'e4_1',
  'e4_half',
	'f4_1',
  'g4_1',
	'g4_half',
  'c5_1_half',
  'd5_1',]

# image being analyzed
image = cv2.imread("images/test.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# index for template descriptors
i = 0
for t in note_files:
  # get note, pitch, and beat
  file_name = t.split("/")[1].split(".")[0]
  beam_check = file_name.split("_")

  if beam_check[0] != "beam":
    note = file_name.split("_")[0][0]
    pitch = file_name.split("_")[0][1]
    beat = file_name[2].split("_")[1]

    if beat == "half":
      beat = 0.5
    else:
      beat = double(beat)
  else:
    file_name


  # load the image image, convert it to grayscalse
  template = cv2.imread(t, 0)
  (tH, tW) = template.shape[:2]

  # loop over the images to find the template in
  # load the image, convert it to grayscale, and initialize the
  # bookkeeping variable to keep track of the matched region
  found = None

  # loop over the scales of the image
  for scale in np.linspace(0.2, 1.5, 80)[::-1]:
    # resize the image according to the scale, and keep track
    # of the ratio of the resizing
    resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
    r = gray.shape[1] / float(resized.shape[1])

    # if the resized image is smaller than the template, then break
    # from the loop
    if resized.shape[0] < tH or resized.shape[1] < tW:
      break

    # apply template matching to find the template in the image
    result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    # threshold for determining if there is a match
    loc = np.where(result >= 0.9)

    # if we have found a new maximum correlation value, then update
    # the bookkeeping variable
    if found is None or maxVal > found[0]:
      found = (maxVal, maxLoc, r, loc)

  # unpack the bookkeeping variable and compute the (x, y) coordinates
  # of the bounding box based on the resized ratio
  (_, maxLoc, r, loc) = found
  
  for (x,y) in zip(loc[1], loc[0]):
    (startX, startY) = (int(x * r), int(y * r))
    (endX, endY) = (int((x + tW) * r), int((y + tH) * r))

    # draw a bounding box around the detected result and display the image
    image = cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv2.putText(image, n[i], (startX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 2)
  i = i + 1
cv2.imwrite("multi-result.png", image)
open_file('multi-result.png')