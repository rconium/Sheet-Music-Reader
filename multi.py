# import the necessary packages
import numpy as np
import argparse
import imutils
import glob
import cv2

note_files = [
    "template/c.png", 
    "template/d.png",
    "template/e.png", 
    "template/f.png",
    "template/g.png",
    "template/a.png", 
    "template/b.png"]

n = [
	'c',
	'd',
	'e',
	'f',
	'g',
	'a',
	'b']


image = cv2.imread("test.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
i = 0
for t in note_files:
  # load the image image, convert it to grayscalse, and detect edges
  template = cv2.imread(t)
  template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
  template = cv2.Canny(template, 50, 200)
  (tH, tW) = template.shape[:2]

  # loop over the images to find the template in
  # load the image, convert it to grayscale, and initialize the
  # bookkeeping variable to keep track of the matched region
  found = None

  # loop over the scales of the image
  for scale in np.linspace(0.2, 1.0, 20)[::-1]:
    # resize the image according to the scale, and keep track
    # of the ratio of the resizing
    resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
    r = gray.shape[1] / float(resized.shape[1])

    # if the resized image is smaller than the template, then break
    # from the loop
    if resized.shape[0] < tH or resized.shape[1] < tW:
      break

    # detect edges in the resized, grayscale image and apply template
    # matching to find the template in the image
    edged = cv2.Canny(resized, 50, 200)
    result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

    # if we have found a new maximum correlation value, then update
    # the bookkeeping variable
    if found is None or maxVal > found[0]:
      found = (maxVal, maxLoc, r)

  # unpack the bookkeeping variable and compute the (x, y) coordinates
  # of the bounding box based on the resized ratio
  (_, maxLoc, r) = found
  (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
  (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

  # draw a bounding box around the detected result and display the image
  image = cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
  cv2.putText(image, n[i], (startX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 2)
  i = i + 1

  
cv2.imwrite("result.png", image)