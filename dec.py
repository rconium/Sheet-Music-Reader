# import the necessary packages
from midiutil.MidiFile3 import MIDIFile

if __name__ == "__main__":

    note_groups = []

    note_groups.append(["a","4","0.5"])
    note_groups.append(["a","4","1"])
    note_groups.append(["a","1","0.5"])

    midi = MIDIFile(1)
     
    track = 0   
    time = 0
    channel = 0
    volume = 100
    
    midi.addTrackName(track, time, "Track")
    midi.addTempo(track, time, 140)

    for note in note_groups:
        duration = 1
        pitch = int(note[1])
        midi.addNote(track,channel,pitch,time,duration,volume)
        time += duration

    midi.addNote(track,channel,pitch,time,4,0)

    # And write it to disk.
    binfile = open("output.mid", 'wb')
    midi.writeFile(binfile)
    binfile.close()