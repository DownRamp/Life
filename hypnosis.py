import sounddevice as sd
import soundfile as sf
import sys
from scipy.io.wavfile import write
import glob
import tkinter.messagebox


def play_song(filename, repeats):
    data, fs = sf.read(filename, dtype='float32') 
    count = 0

    while(count < repeats):
        sd.play(data, fs)
        sd.wait()
        count+=1

    tkinter.messagebox.showinfo("End Of Track",  "End Of Track")


def record():
    fs = 44100
    seconds = 3
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('output.wav', fs, myrecording)


def window(main):
    frame = Frame(main)
    frame.grid()
    # Song selection
    list_songs = glob.glob("Music/*")
    list_items = StringVar(value=list_songs)
    listing = Listbox(frame, listvariable=list_items, height=len(list_songs))
    listing.grid(row=1)

    # record button
    Button(frame, text="Record Internal Message", command=lambda: record())\
        .grid(row=5)

    # enter repeats
    Label(frame, text="Enter number of repeats for music", font=('Aerial 12')).grid(row=6)
    ent = Entry(frame)
    ent.grid(row=7)

    # play
    Button(frame, text="Play", command=lambda: play_song(listing.get(listing.curselection()), ent.get())\
        .grid(row=8)

if __name__ == '__main__':
    selection = input("Input selection: ")
    repeats = input("Amount of repeats: ")
    try:
        play_song(int(selection), int(repeats))
    except:
        print("Incorrect input caused error")
        sys.exit