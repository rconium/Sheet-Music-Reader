# import the necessary packages
import numpy as np
import argparse
import imutils
import glob
import cv2
import sys
import subprocess
import os
from midiutil.MidiFile3 import MIDIFile

#list contains all the notes
notesList = []

#dictionary contains all the notes information with the pixel coordinates as keys
note_locations = {}

# templates list
note_files = [
    "template/rest_sixteenth_quarter.png",
    "template/rest_whole_4.png",
    "template/rest_wholesixt_425.png",
    "template/rest_sixteenth_25.png",
    "template/a4_half.png",
    "template/a4_50.png",
    "template/beam_a4_75_e4_quarter_d4_half.png",
    "template/beam_c4_75_d4_quarter_e4_half.png",
    "template/beam_c4_75_d4_25_e4_half.png",
    "template/beam_a4_75_b4_25_a4_half.png",
    "template/beam_a4_75_b4_quarter_a4_half.png",
    "template/beam_d4_75_c4_quarter_d4_half.png",
    "template/beam_c5_75_b4_25_c5_half.png",
    "template/beam_c5_75_b4_25_a4_half.png",
    "template/beam_c5_75_b4_quarter_a4_half.png",
    "template/beam_c4_75_d4_25_e4_50.png",
    "template/beam_c4_75_d4_quarter_e4_50.png",
    "template/beam_a4_75_e4_quarter_d4_50.png",
    "template/beam_d4_75_c4_quarter_d4_50.png",
    "template/beam_c5_75_b4_25_c5_50.png",
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

# Notes types and pitch dictionary 
note_defs = {
     "g5" : (79),
     "f5" : (77),
     "e5" : (76),
     "d5" : (74),
     "c5" : (72),
     "b4" : (71),
     "a4" : (69),
     "g4" : (67),
     "f4" : (65),
     "e4" : (64),
     "d4" : (62),
     "c4" : (60),
     "b3" : (59),
     "a3" : (57),
     "g3" : (55),
     "f3" : (53),
     "e3" : (52),
     "d3" : (50),
     "c3" : (48),
     "b2" : (47),
     "a2" : (45),
     "f2" : (53),
}

#----------------------------------------------------------------------------------------------------------#
# Function:
# open image files
def open_file(path):
  cmd = {'linux':'eog', 'win32':'explorer', 'darwin':'open'}[sys.platform]
  subprocess.run([cmd, path])

#----------------------------------------------------------------------------------------------------------#
# Function: 
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

#----------------------------------------------------------------------------------------------------------#
# Function: Read take and return the input file
def SelectFile(defaultFile):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    # Select  file, default is prog.asm
    while True:
        imgFile = defaultFile
        print("\nEnter an Image File or Press Enter to Select the Defaul Image (" + str(imgFile) + ")")
        userInput = input()
        if userInput == "":
            userInput = defaultFile
            return userInput
        else:
            imgFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(imgFile):
                print("File does not exist. \n")
            else:
                return userInput

# read image from selected image
image = cv2.imread(SelectFile("images/test.png"))

# image being analyzed
row, col = image.shape[:2]
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

print("Segmenting the image...\n")
cv2.line(image, (0, int(row/4)) , (col, int(row/4)), (0, 0, 255))
cv2.line(image, (0, int(row/2)) , (col, int(row/2)), (0, 0, 255))
cv2.line(image, (0, int(3*row/4)) , (col, int(3*row/4)), (0, 0, 255))

# create image file 
cv2.imwrite("marked_up_sheet.png", image)
open_file('marked_up_sheet.png')

print("\nLoading.......\n")
cmd = {'linux':'eog', 'win32':'explorer', 'darwin':'open'}[sys.platform]
for t in note_files:
  output = []
  # get note, pitch, and beat
  file_name = t.split("/")[1].split(".")[0]
  beam_check = file_name.split("_")

  if beam_check[0] == "rest":
    rest = beam_check[1]
    pitch = 0
    beat = beam_check[2]

    if beat == "425":
      beat = "4.25"
    elif beat == "quarter" or beat == "25":
      beat = "0.25"
    elif beat == "half" or beat == "50":
      beat = "0.5"
    
    output.append([rest, pitch, beat])
    print("Detecting rest" + rest + " with beat of " + beat)

  elif beam_check[0] != "beam":
    note = beam_check[0]
    pitch = note_defs[note]
    beat = file_name.split("_")[1]

    if beat == "half" or beat == "50":
      beat = "0.5"
    elif beat == "1half" or beat == "150":
      beat = "1.5"
    elif beat == "quarter" or beat == "25":
      beat = "0.25"
    elif beat == "75":
      beat = "0.75"

    output.append([note, pitch, beat])
    print("Detecting " + note + " with beat of " + beat)
    
  else:
    size = len(beam_check)
    n_temp = ""
    b_temp = ""
    for i in range(1, size, int((size-1)/3)):
      note = beam_check[i]
      pitch = note_defs[note]
      beat = beam_check[i + 1]

      if beat == "half" or beat == "50":
        beat = "0.5"
      elif beat == "1half" or beat == "150":
        beat = "1.5"
      elif beat == "quarter" or beat == "25":
        beat = "0.25"
      elif beat == "75":
        beat = "0.75"
      
      n_temp = n_temp + "_" + note
      b_temp = b_temp + "_" + beat

      output.append([note, pitch, beat])
    print("Detecting beam" + n_temp + " with beat of " + b_temp)
  
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
  color = list(np.random.choice(range(256), size=3))

  non_repeat = True
  for (x,y) in zip(loc[1], loc[0]):
    (startX, startY) = (int(x * r), int(y * r))

    (endX, endY) = (int((x + tW) * r), int((y + tH) * r))

    # draw a bounding box around the detected result and display the image
    image = cv2.rectangle(image, (startX, startY), (endX, endY), (100, int(color[1]), int(color[2])), 2)

    cv2.putText(image, beam_check[0], (startX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 2)
    note_locations[(startX,startY,endX,endY)] = output
    if non_repeat:
      print("...... Detected!")
      non_repeat = False
  
  if not non_repeat:
    cv2.imwrite('marked_up_sheet.png', image)
    open_file('marked_up_sheet.png')
# breakpoint()

outputFile = open('results/notes.txt', "w")

keys = list(note_locations.keys())

keys = sorted(keys, key = sort_keyval)

print("\nOrdered Notes List:")
print(keys)

# get rid of duplicates
for i in range(0, len(keys), 1):
  if i == 0:
    prev = note_locations[keys[i]]
  else:
    # prev.sort()
    # note_locations[keys[i]].sort()

    if prev == note_locations[keys[i]]:
      del note_locations[keys[i]]
      continue
    else:
      prev = note_locations[keys[i]]

  #print(note_locations[keys[i]])
  outputFile.write(str(note_locations[keys[i]]) + "\n")
  #make a list of all notes
  notesList.append(note_locations[keys[i]])

# DEBUGGING: Show this certain box as yellow
# image = cv2.rectangle(image, (keys[3][0], keys[3][1]), (keys[3][2], keys[3][3]), (0, 255, 255), 2)

# create image file 
# cv2.imwrite("marked_up_sheet.png", image)
# open_file('marked_up_sheet.png')
outputFile.close() 

print("\nMaking midi music file.......\n")
#----------------------------------------------------------------------------------------------------------#
# Output the notes as midi file.

# Create the MIDIFile Object with 1 track
midi = MIDIFile(1)
 
# the first track is 0, here we only need one
track = 0  
time = 0
channel = 0

# Use constant volume for all notes
volume = 100
    
# Add track name and tempo.
midi.addTrackName(track, time, "Track")
midi.addTempo(track, time, 140)

# loop over notes and add the note
for note in notesList:

  #check if the note is beam
  if len(note) > 1:
    for item in note:
        #Get the duration time or beat and get the picth
        duration = float(item[2])
        pitch = int(item[1])

        #add the note to midi object.
        midi.addNote(track,channel,pitch,time,duration,volume)

        #incremnt the time by duration time to add new note and play the notes in order  
        time += duration

  else:
    #Get the duration time or beat and get the picth
    duration = float(note[0][2])
    pitch = int(note[0][1])

    if note[0][0] == "sixteenth" or \
      note[0][0] == "whole" or \
      note[0][0] == "wholesixt":
      midi.addNote(track,channel,pitch,time,duration,0)
      continue

    #add the note to midi object.
    midi.addNote(track,channel,pitch,time,duration,volume)

    #incremnt the time by duration time to add new note and play the notes in order  
    time += duration

#insert sound with volume 0 after the music
midi.addNote(track,channel,pitch,time,4,0)

# Create midi music file
binfile = open("music.mid", 'wb')
midi.writeFile(binfile)
binfile.close()
open_file('music.mid')
