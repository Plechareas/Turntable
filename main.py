import tkinter
from tkinter import filedialog, messagebox
import customtkinter
import pygame
from PIL import Image, ImageTk
from customtkinter import CTkFont
import os
from lyrics import show_lyrics  # Import the show_lyrics function from lyrics.py
from cover_finder import download_album_cover  # Import the download_album_cover function from cover_finder.py

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()
root.title('Turntable')
root.geometry('990 x 670')
root.minsize(990, 670)
root.resizable(False, False)
root.iconbitmap('Icons/Vinyl.ico')
pygame.mixer.init()

SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)
n = 0
is_playing = False
is_seeking = False

# Determine text color based on appearance mode
text_color = '#ffffff' if customtkinter.get_appearance_mode() != "Light" else '#000000'

if customtkinter.get_appearance_mode() == "Light":
    text_color = '#000000'
    bg_color = '#ffffff'
else:
    text_color = '#ffffff'
    bg_color = '#222222'

# Create a label for the song title
song_name_label = tkinter.Label(root, bg='#222222', fg='#ffffff', font=("Helvetica", 10))
song_name_label.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

# Create a frame for the song thumbnails
library_frame = tkinter.Frame(root, bg=root.cget("bg"))
library_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

small_label = None  # Initialize the small_label variable
is_in_library = False

def get_album_cover(song_name, n):
    global small_label
    cover_path = download_album_cover(song_name)
    if cover_path:
        image1 = Image.open(cover_path)
        image2 = image1.resize((280, 280))
        load = ImageTk.PhotoImage(image2)
        label1 = tkinter.Label(root, image=load)
        label1.image = load
        if not is_in_library:
            label1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        else:
            label1.place_forget()

        # Create and place a smaller version of the album cover in the bottom left corner
        small_image = image1.resize((50, 50))
        small_load = ImageTk.PhotoImage(small_image)
        if small_label:
            small_label.config(image=small_load)
            small_label.image = small_load
        else:
            small_label = tkinter.Label(root, image=small_load)
            small_label.image = small_load
            small_label.place(relx=0.05, rely=0.95, anchor=tkinter.SW)
    else:
        label1 = tkinter.Label(root, text="", bg='#222222', fg='#ffffff')
        label1.place(relx=0.19, rely=0.06)

    stripped_string = os.path.splitext(os.path.basename(song_name))[0]
    song_name_label.config(text=stripped_string)

def resize_widgets(event):
    play_button.place_configure(relx=0.5, rely=0.95, anchor=tkinter.CENTER)
    skip_f.place_configure(relx=0.56, rely=0.95, anchor=tkinter.CENTER)
    skip_b.place_configure(relx=0.44, rely=0.95, anchor=tkinter.CENTER)
    next_s.place_configure(relx=0.62, rely=0.95, anchor=tkinter.CENTER)
    prev_s.place_configure(relx=0.38, rely=0.95, anchor=tkinter.CENTER)
    slider.place_configure(relx=0.92, rely=0.95, anchor=tkinter.CENTER)
    mute_button.place_configure(relx=0.84, rely=0.95, anchor=tkinter.CENTER)
    progress_slider.place_configure(relx=0.5, rely=0.88, anchor=tkinter.CENTER)
    current_time_label.place_configure(relx=0.18, rely=0.88, anchor=tkinter.CENTER)
    total_time_label.place_configure(relx=0.81, rely=0.88, anchor=tkinter.CENTER)
    lyrics_button.place_configure(relx=0.8, rely=0.95, anchor=tkinter.CENTER)
    app_name_label.place_configure(relx=0.01, rely=0.01, anchor=tkinter.NW)
    buttons_frame.place_configure(relx=0, rely=0.12, anchor=tkinter.NW)
    library_frame.place_configure(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

root.bind("<Configure>", resize_widgets)

def update_progress():
    if pygame.mixer.music.get_busy() and not is_seeking:
        current_pos = pygame.mixer.music.get_pos() / 1000  # Get current position in seconds
        song_length = pygame.mixer.Sound(list_of_songs[n]).get_length()  # Get song length in seconds
        progress_slider.set(current_pos / song_length)  # Set progress slider value

        # Update the current time label
        current_minutes = int(current_pos // 60)
        current_seconds = int(current_pos % 60)
        current_time_label.config(text=f"{current_minutes}:{current_seconds:02d}")

        # Update the total time label
        total_minutes = int(song_length // 60)
        total_seconds = int(song_length % 60)
        total_time_label.config(text=f"{total_minutes}:{total_seconds:02d}")

    root.after(1000, update_progress)  # Schedule the function to run again after 1 second

def play_music():
    global n, is_playing, is_in_library, small_label
    if is_playing:
        pygame.mixer.music.pause()
        play_button.configure(text='▶')
        is_playing = False
    else:
        if pygame.mixer.music.get_pos() == -1:  # Check if the song is not loaded
            song_name = list_of_songs[n]
            pygame.mixer.music.load(song_name)
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.5)
            get_album_cover(song_name, n)
        else:
            pygame.mixer.music.unpause()
        play_button.configure(text='||')
        is_playing = True
        update_progress()

        # Show the small album cover if in the Library
        if is_in_library:
            cover_path = download_album_cover(list_of_songs[n])
            if cover_path:
                image1 = Image.open(cover_path)
                small_image = image1.resize((50, 50))
                small_load = ImageTk.PhotoImage(small_image)
                if small_label:
                    small_label.config(image=small_load)
                    small_label.image = small_load
                    small_label.place(relx=0.05, rely=0.95, anchor=tkinter.SW)
                else:
                    small_label = tkinter.Label(root, image=small_load)
                    small_label.image = small_load
                    small_label.place(relx=0.05, rely=0.95, anchor=tkinter.SW)


def play_next_song():
    global n, is_playing
    n = (n + 1) % len(list_of_songs)  # Move to the next song, loop back to the start if at the end
    play_selected_song_from_library(n)


def skip_forward():
    current_pos = pygame.mixer.music.get_pos() / 1000  # Get current position in seconds
    new_pos = current_pos + 10  # Skip forward by 10 seconds
    song_length = pygame.mixer.Sound(list_of_songs[n]).get_length()
    if new_pos < song_length:
        pygame.mixer.music.set_pos(new_pos)
    else:
        pygame.mixer.music.set_pos(song_length - 1)  # Set to the end of the song if new_pos exceeds song length

def skip_backwards():
    current_pos = pygame.mixer.music.get_pos() / 1000  # Get current position in seconds
    new_pos = current_pos - 10  # Skip backward by 10 seconds
    if new_pos > 0:
        pygame.mixer.music.set_pos(new_pos)
    else:
        pygame.mixer.music.set_pos(0)  # Set to the start of the song if new_pos is less than 0

def next_song():
    global n, is_playing
    n = (n + 1) % len(list_of_songs)
    song_name = list_of_songs[n]
    pygame.mixer.music.load(song_name)
    pygame.mixer.music.play(loops=0)
    pygame.mixer.music.set_volume(0.5)
    if not is_in_library:
        get_album_cover(song_name, n)
    else:
        # Update the small album cover
        cover_path = download_album_cover(song_name)
        if cover_path:
            image1 = Image.open(cover_path)
            small_image = image1.resize((50, 50))
            small_load = ImageTk.PhotoImage(small_image)
            small_label.config(image=small_load)
            small_label.image = small_load
    play_button.configure(text='||')
    is_playing = True
    update_progress()

def previous_song():
    global n, is_playing
    n = (n - 1) % len(list_of_songs)
    song_name = list_of_songs[n]
    pygame.mixer.music.load(song_name)
    pygame.mixer.music.play(loops=0)
    pygame.mixer.music.set_volume(0.5)
    if not is_in_library:
        get_album_cover(song_name, n)
    else:
        # Update the small album cover
        cover_path = download_album_cover(song_name)
        if cover_path:
            image1 = Image.open(cover_path)
            small_image = image1.resize((50, 50))
            small_load = ImageTk.PhotoImage(small_image)
            small_label.config(image=small_load)
            small_label.image = small_load
    play_button.configure(text='||')
    is_playing = True
    update_progress()

def volume(value):
    pygame.mixer.music.set_volume(float(value))

def seek(value):
    global is_seeking
    is_seeking = True
    song_length = pygame.mixer.Sound(list_of_songs[n]).get_length()  # Get song length in seconds
    new_pos = value * song_length  # Calculate new position in seconds
    pygame.mixer.music.set_pos(new_pos)  # Set new position
    is_seeking = False

def seek_click(event):
    song_length = pygame.mixer.Sound(list_of_songs[n]).get_length()  # Get song length in seconds
    click_position = event.x / progress_slider.winfo_width()  # Get click position as a fraction of the progress slider width
    progress_slider.set(click_position)  # Set the slider to the click position
    seek(click_position)  # Seek to the new position

previous_volume = 0.5  # Variable to store the previous volume level
is_muted = False  # Variable to track mute state

def toggle_mute():
    global is_muted, previous_volume
    if is_muted:
        pygame.mixer.music.set_volume(previous_volume)
        mute_button.configure(text='🔊')
        is_muted = False
    else:
        previous_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(0)
        mute_button.configure(text='🔇')
        is_muted = True

side_window = None

def play_selected_song_from_library(index):
    global n, is_playing, is_in_library, small_label
    n = index
    song_name = list_of_songs[n]
    pygame.mixer.music.load(song_name)
    pygame.mixer.music.play(loops=0)
    pygame.mixer.music.set_volume(0.5)
    cover_path = download_album_cover(song_name)
    if cover_path:
        image1 = Image.open(cover_path)
        image2 = image1.resize((280, 280))
        load = ImageTk.PhotoImage(image2)
        label1 = tkinter.Label(root, image=load)
        label1.image = load
        label1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
    stripped_string = os.path.splitext(os.path.basename(song_name))[0]
    song_name_label.config(text=stripped_string)
    play_button.configure(text='||')
    is_playing = True
    update_progress()

    # Show the song title and album cover, and hide the grid
    song_name_label.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)
    for widget in library_frame.winfo_children():
        widget.destroy()
    is_in_library = False

    # Hide the small album cover
    if small_label:
        small_label.place_forget()

def toggle_song_list():
    global is_in_library, small_label
    is_in_library = True

    # Hide the current album cover and song title
    song_name_label.place_forget()
    for widget in root.winfo_children():
        if isinstance(widget, tkinter.Label) and hasattr(widget, 'image') and widget != small_label:
            widget.place_forget()

    # Clear the library frame
    for widget in library_frame.winfo_children():
        widget.destroy()

    # List to keep references to PhotoImage objects
    image_refs = []

    # Populate the library frame with song thumbnails in a 3x4 grid
    for i, song in enumerate(list_of_songs):
        cover_path = download_album_cover(song)
        if cover_path:
            image1 = Image.open(cover_path)
            image2 = image1.resize((100, 100))
            load = ImageTk.PhotoImage(image2)
            image_refs.append(load)  # Keep a reference to the image
            
            # Create a frame to hold the cover image and title
            frame = tkinter.Frame(library_frame, bg=root.cget("bg"))
            frame.grid(row=i // 3, column=i % 3, padx=10, pady=10)
            
            cover_label = tkinter.Label(frame, image=load)
            cover_label.image = load
            cover_label.pack()

            # Add song title below the cover image
            song_title = os.path.splitext(os.path.basename(song))[0]
            if len(song_title) > 15:  # Truncate title if it's too long
                song_title = song_title[:15] + '...'
            title_label = tkinter.Label(frame, text=song_title, bg=root.cget("bg"), fg='#ffffff', font=("Helvetica", 10))
            title_label.pack()

            cover_label.bind("<Button-1>", lambda e, index=i: play_selected_song_from_library(index))

    # Show the small album cover if a song is playing
    if is_playing:
        cover_path = download_album_cover(list_of_songs[n])
        if cover_path:
            image1 = Image.open(cover_path)
            small_image = image1.resize((50, 50))
            small_load = ImageTk.PhotoImage(small_image)
            if small_label:
                small_label.config(image=small_load)
                small_label.image = small_load
                small_label.place(relx=0.05, rely=0.95, anchor=tkinter.SW)
            else:
                small_label = tkinter.Label(root, image=small_load)
                small_label.image = small_load
                small_label.place(relx=0.05, rely=0.95, anchor=tkinter.SW)

def open_folder():
    global is_in_library
    is_in_library = False

    folder_selected = filedialog.askdirectory()
    if folder_selected:
        global list_of_songs
        list_of_songs = [os.path.join(folder_selected, f) for f in os.listdir(folder_selected) if f.endswith(('.mp3', '.wav'))]
        if not list_of_songs:
            messagebox.showinfo("No Songs Found", "The selected folder contains no songs.")
            return
        if list_of_songs:
            n = 0
            song_name = list_of_songs[n]
            pygame.mixer.music.load(song_name)
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.5)
            get_album_cover(song_name, n)
            play_button.configure(text='||')
            is_playing = True
            update_progress()

# Buttons
large_font = CTkFont(size=17)
play_button = customtkinter.CTkButton(master=root, text='▶', command=play_music, width=50, height=40, font=large_font)
play_button.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)

large_font = CTkFont(size=17)
skip_f = customtkinter.CTkButton(master=root, text='↻', command=skip_forward, width=40, height=30,font=large_font)
skip_f.place(relx=0.71, rely=0.95, anchor=tkinter.CENTER)

large_font = CTkFont(size=17)
skip_b = customtkinter.CTkButton(master=root, text='↺', command=skip_backwards, width=40, height=30,font=large_font)
skip_b.place(relx=0.29, rely=0.95, anchor=tkinter.CENTER)

large_font = CTkFont(size=17)
next_s = customtkinter.CTkButton(master=root, text='>>', command=next_song, width=40, height=30,font=large_font)
next_s.place(relx=0.83, rely=0.95, anchor=tkinter.CENTER)

large_font = CTkFont(size=17)
prev_s = customtkinter.CTkButton(master=root, text='<<', command=previous_song, width=40, height=30,font=large_font)
prev_s.place(relx=0.17, rely=0.95, anchor=tkinter.CENTER)

slider = customtkinter.CTkSlider(master=root, from_=0, to=1, command=volume,width=120)
slider.place(relx=0.9, rely=0.25, anchor=tkinter.CENTER)

large_font = CTkFont(size=18)
medium_font = CTkFont(size=20)

mute_button = customtkinter.CTkButton(master=root, text='🔊', command=toggle_mute, width=33, height=33,font=large_font)
mute_button.place(relx=0.9, rely=0.59, anchor=tkinter.CENTER)

# Add labels for current time and total time
current_time_label = tkinter.Label(root, text='0:00', bg=root.cget("bg"), fg='#ffffff', font=("Helvetica",8))
current_time_label.place(relx=1, rely=0.98, anchor=tkinter.CENTER)

total_time_label = tkinter.Label(root, text='0:00', bg=root.cget("bg"), fg='#ffffff', font=("Helvetica", 8))
total_time_label.place(relx=0.9, rely=0.88, anchor=tkinter.CENTER)

# Increase the width of the progress slider
progress_slider = customtkinter.CTkSlider(master=root, from_=0, to=1, command=seek, width=550)
progress_slider.place(relx=0.5, rely=0.88, anchor=tkinter.CENTER)
progress_slider.set(0)

# Bind the click and drag events to the progress slider
progress_slider.bind("<Button-1>", seek_click)
progress_slider.bind("<B1-Motion>", lambda event: seek(progress_slider.get()))

# Add the lyrics button below the folder button
lyrics_button = customtkinter.CTkButton(master=root, text='🎤', command=lambda: show_lyrics(root, list_of_songs, n), font=large_font, width=33, height=33)
lyrics_button.place(relx=0.9, rely=0.93, anchor=tkinter.CENTER)

# Add the app name label
app_name_label = tkinter.Label(root, text='Turntable', bg=root.cget("bg"), fg='#ffffff', font=("Helvetica", 30))
app_name_label.place(relx=0.05, rely=0.05, anchor=tkinter.NW)

# Create a frame for the buttons
buttons_frame = tkinter.Frame(root,bg=root.cget("bg"))
buttons_frame.place(relx=0.05, rely=0.12, anchor=tkinter.NW)

# Add the library label
library_label = tkinter.Label(buttons_frame, text='🕮Library', bg=root.cget("bg"), fg='#ffffff', font=("Helvetica", 20))
library_label.pack(fill=tkinter.X, pady=(40))
library_label.bind("<Button-1>", lambda e: toggle_song_list())
library_label.bind("<Enter>", lambda e: library_label.config(fg='#606060'))
library_label.bind("<Leave>", lambda e: library_label.config(fg='#ffffff'))

# Add the explore label
explore_label = tkinter.Label(buttons_frame, text='🔎Explore', bg=root.cget("bg"), fg='#ffffff', font=("Helvetica", 20))
explore_label.pack(fill=tkinter.X, pady=(40))
explore_label.bind("<Button-1>", lambda e: open_folder())
explore_label.bind("<Enter>", lambda e: explore_label.config(fg='#606060'))
explore_label.bind("<Leave>", lambda e: explore_label.config(fg='#ffffff'))

# Add the profile label
profile_label = tkinter.Label(buttons_frame, text='👤Profile', bg=root.cget("bg"), fg='#ffffff', font=("Helvetica", 20))
profile_label.pack(fill=tkinter.X, pady=(40))
profile_label.bind("<Enter>", lambda e: profile_label.config(fg='#606060'))
profile_label.bind("<Leave>", lambda e: profile_label.config(fg='#ffffff'))

root.mainloop()