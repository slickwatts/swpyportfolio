# ===============================================
#           YouTube Downloader GUI
#
# Author: Slick
# Date  :
# ===============================================
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Notebook
import youtube_search
import youtube_dl as ytd
#import yt_dwnld
import requests
import os
from PIL import Image, ImageTk


class YTDownloader:
    """YouTube downloader class"""
    BASE_URL = "https://www.youtube.com"

    def __init__(self):
        self.downloader = ytd.YoutubeDL()

    def search(self, search_phrase):
        """Returns a list of tuples containing TITLE, DURATION, and URL_SUFFIX
           of the videos searched for"""
        results = youtube_search.YoutubeSearch(search_phrase).to_dict()
        video_data = [(v['title'], v['duration'], v['url_suffix'], v['thumbnails'][0]) for v in results]
        return video_data

    def download(self, url):
        """Downloads a YouTube video using its URL"""
        self.downloader.download([url])


class DownloaderApp:
    def __init__(self):
        self.win = Tk()
        self.win.title('YouTube Downloader')
        self.win.geometry('700x550')
        self.win.resizable(False, False)
        self.pic_dir = '/home/slick/Pictures/yt_temp/'
        self.download_dir = '/home/slick/Downloads'
        self.downloader = YTDownloader()
        self.add_widgets()

    def add_widgets(self):
        # ADD TABS
        self.tab_configure = Notebook(self.win)
        self.tab1 = Frame(self.tab_configure, bg='black')
        self.tab2 = Frame(self.tab_configure, bg='black')
        self.tab_configure.add(self.tab1, text="Download")
        self.tab_configure.add(self.tab2, text="Settings")
        self.tab_configure.pack(expand=1, fill=BOTH)

        # ADD FRAMES
        # -main frames
        self.frame_top_tab1 = Frame(self.tab1, bg='grey')
        self.frame_mid_tab1 = Frame(self.tab1, bg='grey')
        self.frame_bot_tab1 = Frame(self.tab1, bg='grey')
        self.frame_tab2     = Frame(self.tab2, bg='#F4511E')
        self.frame_top_tab1.pack(expand=1, fill=BOTH, padx=5, pady=2.5)
        self.frame_mid_tab1.pack(expand=1, fill=BOTH, padx=5, pady=2.5)
        self.frame_bot_tab1.pack(expand=1, fill=BOTH, padx=5, pady=2.5)
        self.frame_tab2.pack(expand=1, fill=BOTH, padx=5, pady=2.5)
        # -sub frames
        self.frame_top_L_tab1 = Frame(self.frame_top_tab1, bg='black')
        self.frame_top_R_tab1 = Frame(self.frame_top_tab1, bg='black')
        self.frame_bot_L_tab1 = LabelFrame(self.frame_bot_tab1, bg='black',
                                           text='Search Results', fg='white')
        self.frame_bot_R_tab1 = LabelFrame(self.frame_bot_tab1, bg='black',
                                           text='Video Selector', fg='white')
        self.frame_top_L_tab1.pack(side=LEFT, expand=1, fill=BOTH, padx=2, pady=2.5)
        self.frame_top_R_tab1.pack(side=RIGHT, expand=1, fill=BOTH, padx=2, pady=2.5)
        self.frame_bot_L_tab1.pack(side=LEFT, expand=1, fill=BOTH, padx=2, pady=2.5)
        self.frame_bot_R_tab1.pack(side=RIGHT, expand=1, fill=BOTH, padx=2, pady=2.5)

        # ADD WIDGETS
        # -top right frame 1
        self.vid_title_var = StringVar()
        self.vid_dur_var = StringVar()
        self.title_label = Label(self.frame_top_R_tab1, text='Title', bg='black',
                                 fg='white', font=('arial', 11))
        self.select_video_title = Label(self.frame_top_R_tab1, text='',
                                        textvariable=self.vid_title_var, bg='black',
                                        fg='white', wraplength=200)
        self.time_label = Label(self.frame_top_R_tab1, text='Duration', bg='black',
                                fg='white', font=('arial', 11))
        self.select_vid_duration = Label(self.frame_top_R_tab1, text='',
                                         textvariable=self.vid_dur_var, bg='black',
                                         fg='white')
        self.download_button = Button(self.frame_top_R_tab1, text='Download', bg='black',
                                      fg='white', bd=2, relief=RAISED, command=self.download)
        self.title_label.grid(row=0, column=0, padx=5, pady=30)
        self.time_label.grid(row=1, column=0, padx=5, pady=30)
        self.select_video_title.grid(row=0, column=1, padx=50, pady=30)
        self.select_vid_duration.grid(row=1, column=1, padx=50, pady=30)
        self.download_button.grid(row=2, column=1, pady=10)

        # -mid frame
        self.vid_search_url = StringVar()
        self.search_entry = Entry(self.frame_mid_tab1, width=45, font=('arial', 12),
                                  bd=4, bg='black', fg='white', highlightbackground='black',
                                  textvariable=self.vid_search_url)
        self.entry_pad = Label(self.frame_mid_tab1, text='  ', bg='grey')
        self.search_button = Button(self.frame_mid_tab1, text='Search', bg='black',
                                    fg='white', bd=2, relief=RAISED, command=self.search)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)
        self.entry_pad.grid(row=0, column=0)
        self.search_button.grid(row=0, column=2, padx=20)

        # -bottom frame left
        self.video_choices = ScrolledText(self.frame_bot_L_tab1, width=30, height=10 ,
                                          bg='black', fg='white', highlightbackground='black',
                                          font=('arial', 15))
        self.video_choices.pack(expand=1, fill=BOTH)

        # -bottom frame right
        self.vid_index_var = IntVar()
        self.vid_index_picker = Spinbox(self.frame_bot_R_tab1, values=list(range(1, 26)),
                                        width=2, textvariable=self.vid_index_var,
                                        font=('arial', 11))
        self.vid_select_button = Button(self.frame_bot_R_tab1, text='Select', bd=2,
                                        relief=RAISED, bg='black', fg='white',
                                        highlightbackground='black', command=self.select)
        self.vid_index_picker.pack(pady=25)
        self.vid_select_button.pack(pady=15)

    def search(self):
        try:
            self.results = self.downloader.search(search_phrase=self.search_entry.get())
            self.video_choices.delete('1.0', END)
            for i, video in enumerate(self.results):
                self.video_choices.insert(INSERT, f'VIDEO #{i+1}\n')
                for info in video[:2]:
                    self.video_choices.insert(INSERT, info + '\n')
                self.video_choices.insert(INSERT, '\n')
        except KeyError:
            messagebox.showerror(title='Error', message='You gotta search SOMETHING duh...')

    def select(self):
        try:
            index = self.vid_index_var.get() - 1
            title = self.results[index][0]
            duration = self.results[index][1]
            pic_url = self.results[index][3]
            self.vid_title_var.set(title)
            self.vid_dur_var.set(duration)

            # putting picture up
            response = requests.get(pic_url)
            with open(self.pic_dir + 'yt_temp_pic', 'wb') as file:
                file.write(response.content)
            pic = Image.open(self.pic_dir + 'yt_temp_pic')
            render = ImageTk.PhotoImage(pic)
            img = Label(self.frame_top_L_tab1, image=render)
            img.image = render
            img.place(x=0, y=0)
        except AttributeError:
            messagebox.showerror("Error", "Search for videos first.")

    def download(self):
        try:
            os.chdir(self.download_dir)
            index = self.vid_index_var.get() - 1
            suffix = self.results[index][2]
            messagebox.showinfo("Downloading...", "Please wait while it jacks all that shit.\nJust hit OK and we'll start")
            self.downloader.download(self.downloader.BASE_URL + suffix)
            messagebox.showinfo("Success!", "Download completed.")
        except AttributeError:
            messagebox.showerror("Error", "Select video first.")


app = DownloaderApp()
app.win.mainloop()
