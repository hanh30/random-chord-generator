import streamlit as st
import random
from music21 import note, interval, chord, meter, stream, environment
from PIL import Image
import os
import numpy as np
from copy import deepcopy
# import subprocess

# os.system('Xvfb :1 -screen 0 1600x1200x16  &')    # create virtual display with size 1600x1200 and 16 bit color. Color can be changed to 24 or 8
# os.environ['DISPLAY']=':1.0'  # tell X clients to use our virtual DISPLAY :1.0

environment.set('musescoreDirectPNGPath', '/usr/bin/mscore')

os.environ['QT_QPA_PLATFORM'] = 'offscreen'
# subprocess.run(["export", "QT_QPA_PLATFORM=offscreen"])

# subprocess.run(["chmod", "+x", "/mount/src/random-chord-generator/src/random_chords/musescore_setup.sh"])
# subprocess.run(["/mount/src/random-chord-generator/src/random_chords/musescore_setup.sh"], shell=True)

chord_roots = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
pitch_list = ['2', '3']
interval_dict = {
    '': ['M3', 'P5'],
    'm': ['m3', 'P5'],
    'aug': ['M3', 'A5'],
    'dim': ['m3', 'd5'],
    '7': ['M3', 'P5', 'm7'],
    'M7': ['M3', 'P5', 'M7'],
    'm7': ['m3', 'P5', 'm7'],
}

# Function to generate a random chord
def generate_random_chord(chord_roots, interval_dict):
    root_str = random.choice(chord_roots)
    chord_str = random.choice(list(interval_dict.keys()))
    chord_name = root_str + chord_str

    pitch_str = random.choice(pitch_list)
    root = note.Note(root_str + pitch_str)
    note_list = [root]
    for i in interval_dict[chord_str]:
        note_list.append(interval.transposeNote(root, i))
    random.shuffle(note_list)
    chord_note = chord.Chord(note_list)
    chord_note.inversion(random.choice(np.arange(len(chord_note))))

    return chord_name, chord_note

# Create a music stream and add random chords
def create_music_stream(chord_roots, interval_dict, num_chords=10):
    music_stream = stream.Stream()
    music_stream.timeSignature = meter.TimeSignature('1/4')
    
    music_stream_lyric = stream.Stream()
    music_stream_lyric.timeSignature = meter.TimeSignature('1/4')

    for _ in range(num_chords):  # Generating 8 random chords
        chord_name, chord_note = generate_random_chord(chord_roots, interval_dict)
        music_stream.append(chord_note)

        chord_note_lyric = deepcopy(chord_note)
        chord_note_lyric.lyric = chord_name
        music_stream_lyric.append(chord_note_lyric)        

    return music_stream, music_stream_lyric

# Save the music stream as an image
def save_music_stream_as_image(music_stream, file_path):
    music_stream.write('musicxml.png', fp=file_path)


st.title("Random Chord Generator")

chord_roots_filter = st.multiselect(
    "Select chord roots:",
    chord_roots,
    default=chord_roots
)

interval_dict_key_filter = st.multiselect(
    "Select chord type:",
    interval_dict.keys(),
    default=['', 'm']
)

interval_dict_filter = {k:v for (k, v) in interval_dict.items() if k in interval_dict_key_filter}

def show_image():
    if not st.session_state.toggle:
        imageLocation.image(image)
    else:
        imageLocation.image(image_lyric)
        
st.toggle("Show chord names", key='toggle', on_change=show_image)

if st.button('Generate Chords'):
    # Create a music stream
    music_stream, music_stream_lyric = create_music_stream(chord_roots=chord_roots_filter, interval_dict=interval_dict_filter, num_chords=50)

    # Save the music stream as a PNG image
    folder = './output'
    filename = 'random_chords'
    image_path = f'{folder}/{filename}.png'
    image_path_lyric = f'{folder}/{filename}_lyric.png'
    save_music_stream_as_image(music_stream, image_path)
    save_music_stream_as_image(music_stream_lyric, image_path_lyric)
    
    # Display the image
    image_path = f'{folder}/{filename}-1.png'
    image_path_lyric = f'{folder}/{filename}_lyric-1.png'

    image = Image.open(image_path)
    image_lyric = Image.open(image_path_lyric)

    imageLocation = st.empty()
    imageLocation.image(image)




    
