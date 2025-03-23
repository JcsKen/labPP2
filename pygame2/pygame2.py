import pygame
import os

# Initialize pygame mixer and pygame
pygame.init()
pygame.mixer.init()

# Get the absolute path of the current script
directory = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(directory, "music")

# Check if the music folder exists
if not os.path.exists(MUSIC_DIR):
    print(f"Error: Music folder not found at {MUSIC_DIR}")
    exit()

# Get list of MP3 files
songs = [f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")]

# Check if there are songs available
if not songs:
    print("No songs found in the 'music' folder.")
    exit()

# Sort songs to ensure consistent order
songs.sort()
current_song_index = 0

# Load and play the first song
def play_song():
    song_path = os.path.join(MUSIC_DIR, songs[current_song_index])
    print(f"Loading: {song_path}")
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    print(f"Playing: {songs[current_song_index]}")

play_song()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Play/Pause
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    print("Paused")
                else:
                    pygame.mixer.music.unpause()
                    print("Resumed")
            elif event.key == pygame.K_s:  # Stop
                pygame.mixer.music.stop()
                print("Stopped")
            elif event.key == pygame.K_n:  # Next song
                current_song_index = (current_song_index + 1) % len(songs)
                play_song()
            elif event.key == pygame.K_p:  # Previous song
                current_song_index = (current_song_index - 1) % len(songs)
                play_song()

pygame.quit()