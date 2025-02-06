import os
import tkinter
import webbrowser

def show_lyrics(root, list_of_songs, n):
    song_name = os.path.basename(list_of_songs[n]).replace('.wav', '').replace('.mp3', '')
    search_query = f"{song_name} lyrics"
    search_url = f"https://www.google.com/search?q={search_query}"
    
    # Get the position of the main window
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    
    # Calculate the position for the new window
    new_window_x = root_x
    new_window_y = root_y + root_height + 10  # 10 pixels below the main window
    new_window_width = 400
    new_window_height = 400
    
    # Open the browser window with the specified size and position
    webbrowser.open_new(f"{search_url}")