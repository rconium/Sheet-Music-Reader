# import the necessary packages
from midiutil.MidiFile3 import MIDIFile

if __name__ == "__main__":

    note_groups = []

    note_groups.append("a")
    note_groups.append("2")
    note_groups.append("0.5")

    midi = MIDIFile(1)
     
    track = 0   
    time = 0
    channel = 0
    volume = 100

    

    # And write it to disk.
    binfile = open("output.mid", 'wb')
    midi.writeFile(binfile)
    binfile.close()
    open_file('output.mid')
