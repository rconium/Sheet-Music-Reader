import cv2
import numpy as np
from matplotlib import pyplot as plt


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
	
note_imgs = [cv2.imread(note_file, 0) for note_file in note_files]

img_rgb = cv2.imread('scale.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

i = 0
for template in note_imgs:
	w, h = template.shape[::-1]

	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	threshold = .9
	loc = np.where( res >= threshold)
	for pt in zip(*loc[::-1]):
			image = cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
			cv2.putText(image, n[i], pt, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 2)
	i = i + 1
cv2.imwrite('res.png',img_rgb)
