# import the necessary packages
import numpy as np
import argparse
import imutils
import glob
import cv2
import sys
import subprocess
<<<<<<< HEAD

=======
import os
from midiutil.MidiFile3 import MIDIFile

notesList = []

# open image files
>>>>>>> Tarek
def open_file(path):
  cmd = {'linux':'eog', 'win32':'explorer', 'darwin':'open'}[sys.platform]
  subprocess.run([cmd, path])

<<<<<<< HEAD
# templates list
note_files = [
    "template/beam_c4_2_d4_quarter_e4_1.png",
    "template/beam_a4_1half_b4_quarter_a4_1.png",
=======
# sorts coordinates from top left to bottom right.
# uses the sections of each staves as reference to generate the 'location' of the note.
def sort_keyval(x):
  if (x[1] <= row/4):
    return (col) + x[0]
  elif (x[1] <= row/2):
    return (col*2) + x[0]
  elif (x[1] <= 3*row/4):
    return (col*3) + x[0]
  else:
    return (col*4) + x[0]

# templates list
note_files = [
    "template/beam_c4_75_d4_quarter_e4_1.png",
    "template/beam_a4_1half_b4_quarter_a4_1.png",
    "template/beam_d4_75_c4_quarter_d4_half.png",
>>>>>>> Tarek
    "template/b3_1.png",
    "template/c4_half.png",
    "template/d4_3.png",
    "template/d4_half.png",
    "template/e4_1.png",
    "template/e4_half.png",
    "template/f4_1.png",
    "template/g4_1.png",
    "template/g4_half.png",
    "template/c5_1half.png",
    "template/d5_1.png",]

<<<<<<< HEAD
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
  'c5_1half',
  'd5_1',]


# image being analyzed
image = cv2.imread("images/test.png")
row, col = image.shape[:2]
# temp = [None] * height * width
=======
# Function: Read take and return the input file
def SelectFile(defaultFile):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    # Select  file, default is prog.asm
    while True:
        cktFile = defaultFile
        print("\nEnter an Image File or Press Enter to Select the Defaul Image (" + str(cktFile) + ")")
        userInput = input()
        if userInput == "":
            userInput = defaultFile
            return userInput
        else:
            cktFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(cktFile):
                print("File does not exist. \n")
            else:
                return userInput

# image being analyzed
image = cv2.imread(SelectFile("images/test.png"))
row, col = image.shape[:2]
>>>>>>> Tarek
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

note_locations = {}

<<<<<<< HEAD
# index for template descriptors
# i = 0
for t in note_files:
=======
print("\nLoading.......")

for t in note_files:
  
>>>>>>> Tarek
  output = []
  # get note, pitch, and beat
  file_name = t.split("/")[1].split(".")[0]
  beam_check = file_name.split("_")

  if beam_check[0] != "beam":
    note = file_name.split("_")[0][0]
    pitch = file_name.split("_")[0][1]
    beat = file_name.split("_")[1]

    if beat == "half":
      beat = "0.5"
    elif beat == "1half":
      beat = "1.5"
    elif beat == "quarter":
      beat = "0.25"
<<<<<<< HEAD
=======
    elif beat == "75":
      beat = "0.75"
>>>>>>> Tarek

    output.append([note, pitch, beat])
    
  else:
    size = len(beam_check)
    for i in range(1, size, int((size-1)/3)):
      note = beam_check[i][0]
      pitch = beam_check[i][1]
      beat = beam_check[i + 1]

      if beat == "half":
        beat = "0.5"
      elif beat == "1half":
        beat = "1.5"
      elif beat == "quarter":
        beat = "0.25"
<<<<<<< HEAD
=======
      elif beat == "75":
        beat = "0.75"

>>>>>>> Tarek

      output.append([note, pitch, beat])


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
<<<<<<< HEAD

  for (x,y) in zip(loc[1], loc[0]):
    (startX, startY) = (int(x * r), int(y * r))
    (endX, endY) = (int((x + tW) * r), int((y + tH) * r))

    # draw a bounding box around the detected result and display the image
    image = cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv2.putText(image, beam_check[0], (startX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 2)
    note_locations[str((x,y))] = output
  # i = i + 1
# note_locations = list(filter(None, temp))
breakpoint()

outputFile = open('notes.txt', "w")

keys = note_locations.keys()

for i in range(1, row, 1):
  for j in range(1, col, 1):
    curr = ('(' + str(j) + ', ' + str(i) + ')')

    if curr in keys:
      print(curr)
      print(note_locations[curr])

cv2.imwrite("multi-result.png", image)
open_file('multi-result.png')
outputFile.close()
=======
  color = list(np.random.choice(range(256), size=3))

  for (x,y) in zip(loc[1], loc[0]):
    (startX, startY) = (int(x * r), int(y * r))

    (endX, endY) = (int((x + tW) * r), int((y + tH) * r))

    # draw a bounding box around the detected result and display the image
    # if (startY <= row/4):
    #   image = cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
    # elif (startY <= row/2):
    #   image = cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 255), 2)
    # elif (startY <= 3*row/4):
    #   image = cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 255), 2)
    # else:
    #   image = cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 0), 2)
    image = cv2.rectangle(image, (startX, startY), (endX, endY), (100, int(color[1]), int(color[2])), 2)

    cv2.putText(image, beam_check[0], (startX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 2)
    note_locations[(startX,startY,endX,endY)] = output
# breakpoint()

outputFile = open('notes.txt', "w")

keys = list(note_locations.keys())

keys = sorted(keys, key = sort_keyval)

print(keys)

# get rid of duplicates
for i in range(0, len(keys), 1):
  if i == 0:
    prev = note_locations[keys[i]]
  else:
    prev.sort()
    note_locations[keys[i]].sort()

    if prev == note_locations[keys[i]]:
      del note_locations[keys[i]]
      continue
    else:
      prev = note_locations[keys[i]]
  #print(note_locations[keys[i]])
  outputFile.write(str(note_locations[keys[i]]) + "\n")
  notesList.append(note_locations[keys[i]])


cv2.line(image, (0, int(row/4)) , (col, int(row/4)), (0, 0, 255))
cv2.line(image, (0, int(row/2)) , (col, int(row/2)), (0, 0, 255))
cv2.line(image, (0, int(3*row/4)) , (col, int(3*row/4)), (0, 0, 255))

# DEBUGGING: Show this certain box as yellow
# image = cv2.rectangle(image, (keys[3][0], keys[3][1]), (keys[3][2], keys[3][3]), (0, 255, 255), 2)

cv2.imwrite("multi-result.png", image)
open_file('multi-result.png')
outputFile.close() 

midi = MIDIFile(1)
     
track = 0   
time = 0
channel = 0
volume = 100
    
midi.addTrackName(track, time, "Track")
midi.addTempo(track, time, 140)

for note in notesList:
    if len(note) > 1:
        print("beam -_- ")

    else:
        duration = float(note[0][2])
        pitch = int(note[0][1])
        midi.addNote(track,channel,pitch,time,duration,volume)
        time += duration

#insert sound with volume 0 after the music
midi.addNote(track,channel,pitch,time,4,0)

# And write it to disk.
binfile = open("music.mid", 'wb')
midi.writeFile(binfile)
binfile.close()
>>>>>>> Tarek
