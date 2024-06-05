import streamlit as st
import random
from music21 import note, interval, chord, stream
from PIL import Image
import subprocess



subprocess.run(["chmod", "+x", "/mount/src/random-chord-generator/src/random_chords/musescore_setup.sh"])
subprocess.run(["/mount/src/random-chord-generator/src/random_chords/musescore_setup.sh"], shell=True)

chord_roots = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
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
def generate_random_chord():
    root_str = random.choice(chord_roots)
    chord_str = random.choice(list(interval_dict.keys()))
    chord_name = root_str + chord_str

    root = note.Note(root_str)
    note_list = [root]
    for i in interval_dict[chord_str]:
        note_list.append(interval.transposeNote(root, i))
    chord_note = chord.Chord(note_list)

    return chord_name, chord_note

# Create a music stream and add random chords
def create_music_stream(num_chords=10):
    music_stream = stream.Stream()

    for _ in range(num_chords):  # Generating 8 random chords
        chord_name, chord_note = generate_random_chord()
        chord_note.lyric = chord_name
        music_stream.append(chord_note)

    return music_stream

# Save the music stream as an image
def save_music_stream_as_image(music_stream, file_path):
    music_stream.write('musicxml.png', fp=file_path)


st.title("Random Chord Generator")

if st.button('Generate Chords'):
    # Create a music stream
    music_stream = create_music_stream(num_chords=50)

    # Save the music stream as a PNG image
    folder = './output'
    filename = 'random_chords'
    image_path = f'{folder}/{filename}.png'
    save_music_stream_as_image(music_stream, image_path)
    
    # Display the image
    image_path = f'{folder}/{filename}-1.png'
    image = Image.open(image_path)
    st.image(image, caption='Generated Chords', use_column_width=True)
