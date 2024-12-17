import time
import tkinter
from pytubefix import YouTube
import os
import scrapetube
from customtkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
from moviepy  import *
from  tkinter import filedialog

HomeDirectory = os.path.expanduser('~')

app = CTk()
app.title('Youtube Downloader V3')  # Corrected title setting
#app.iconbitmap('youtube.ico')
app.geometry('1920x1080')

# Entry box for search query
EntryBox = CTkEntry(master=app, placeholder_text='What do you want to watch?', width=200)
EntryBox.place(relx=0.1, rely=0.1)

# Option menu for selecting YouTube or YouTube Kids
platform_var = StringVar(value='YouTube')
platform_menu = CTkOptionMenu(master=app, variable=platform_var, values=['YouTube', 'YouTube Kids'])
platform_menu.place(relx=0.1, rely=0.15)

# Option menu for selecting MP3 or MP4 format
format_var = StringVar(value='MP4')
format_menu = CTkOptionMenu(master=app, variable=format_var, values=['MP4', 'MP3'])
format_menu.place(relx=0.1, rely=0.2)

# Scrollable frame for video results
scrollframe = CTkScrollableFrame(master=app, width=750, height=450)
scrollframe.place(relx=0.67, rely=0.45, anchor='center')

def SearchVideos(SearchWord):
    vids = scrapetube.get_search(SearchWord, 10)
    return vids

def CreateDownloadButton(VideoTitle, VideoAuthor, DownloadUrl, ThumbnailUrl):
    response = requests.get(ThumbnailUrl)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((240, 180), Image.LANCZOS)  # Increased thumbnail size
    photo = ImageTk.PhotoImage(img)

    frame = CTkFrame(master=scrollframe)
    frame.pack(pady=5, padx=5, fill='x')

    label = CTkLabel(master=frame, image=photo, text="")
    label.image = photo  # Keep a reference to avoid garbage collection
    label.pack(side='left')

    button = CTkButton(master=frame, text=VideoTitle + ', by: ' + VideoAuthor,
                       command=lambda url=DownloadUrl: DownloadVideo(url))
    button.pack(side='left', padx=10)

def SelectVideos(Query):
    Videos = SearchVideos(Query)
    print(Videos)
    for video in Videos:
        VideoUrl = 'https://www.youtube.com/watch?v=' + video['videoId']
        print(VideoUrl)
        video = YouTube(VideoUrl)
        ThumbnailUrl = video.thumbnail_url
        CreateDownloadButton(video.title, video.author, VideoUrl, ThumbnailUrl)

def DownloadVideo(VideoUrl):
    yt = YouTube(VideoUrl, 'MWEB' if platform_var.get() == 'YouTube Kids' else 'WEB')
    if format_var.get() == 'MP4':
        Yd = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        Yd.download(HomeDirectory + '/Downloads')
    else:
        Yd = yt.streams.filter().get_lowest_resolution()
        Download = Yd.download(HomeDirectory + '/Downloads')
        DownloadSplit = os.path.splitext(Download)[0]
        time.sleep(1)
        video = VideoFileClip(Download)
        audio = video.audio
        audio.write_audiofile(DownloadSplit + 'audio.mp3')
        video.close()
        os.remove(Download)




def test(query):
    for widget in scrollframe.winfo_children():
        widget.destroy()
    SelectVideos(query)

btn = CTkButton(master=app, text='Search', command=lambda: test(EntryBox.get()))
btn.place(relx=0.125, rely=0.25)

app.mainloop()
