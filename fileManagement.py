import os
import shutil
import tkinter
from tkinter import filedialog
from tinytag import TinyTag

import Constants as C

#No Tkinter window opens
tkinter.Tk().withdraw()

class FileManager():
    def __init__(self):
        pass

    #Opens file explorer to find file
    def choose_file(self):
        filename = filedialog.askopenfilename()
        return filename

    #Adds new file to uploadedMusic folder
    def new_file(self, filename):
        if self.check_music_file(filename):
            if not self.file_exists(filename):
                try:
                    shutil.copy(filename, C.MUSIC_FILES)
                    print("Success")
                    return True
                except shutil.SameFileError:
                    print("Source and destination represents the same file.")
                    return False
                except PermissionError:
                    print("Permission denied.")
                    return False
                except:
                    print("Error occurred while copying file.")
                    return False
            else:
                print("This song has already been uploaded")
                return False
        else:
            print("Must be an .mp3, .wav, or .ogg song")
            return False

    #Check if file is in uploadedMusic folder already
    def file_exists(self, filename):
        file_basename = self.convert_to_basename(filename)
        return os.path.exists(os.path.join(C.MUSIC_FILES, file_basename))

    #Delete file from uploadedMusic folder
    def delete_file(self, filename):
        file_basename = self.convert_to_basename(filename)
        file = os.path.join(C.MUSIC_FILES, file_basename)
        if self.file_exists(file):
            try:
                os.remove(file)
                print(f"File '{file_basename}' deleted successfully.")
            except FileNotFoundError:
                print(f"File '{file_basename}' not found.")
            except PermissionError:
                print(f"You don't have permission to delete '{file_basename}'.")
            except Exception as e:
                print(f"An error occurred: {e}")

    #Checks if file is a music file
    def check_music_file(self, filename):
        ext = os.path.splitext(filename)[1]
        if ext == ".mp3" or ext == ".wav" or ext == ".ogg":
            return True
        return False

    #Returns list of already uploaded songs
    def uploaded_songs(self):
        dir = os.listdir(C.MUSIC_FILES)
        if len(dir) == 0:
            raise ValueError
        else:
            return dir 

    def convert_to_basename(self, filename):
        return os.path.basename(filename)

    def temp_title(self, filename):
        return os.path.splitext(filename)[0]
    
class Metadata():
    def __init__(self):
        self.selected_song = None

    def set_selected_song(self, song):
        self.selected_song = song

    def get_title(self):
        audio = TinyTag.get(self.selected_song)
        return audio.title
    
    def get_artist(self):
        audio = TinyTag.get(self.selected_song)
        return audio.artist
    
    def get_duration(self):
        audio = TinyTag.get(self.selected_song)
        return audio.duration