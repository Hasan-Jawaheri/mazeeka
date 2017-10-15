# -*- coding: utf-8 -*-

import sys
import os
import requests
import json
import pafy
from multiprocessing import Pool
import mazeeka_purifier

PLAYLIST = "PLPBVXKmDPYk1dm-gElmWafOzf_BVpHOZm"
PLAYLIST_PATH = os.path.join("playlists", PLAYLIST)
URL = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=" + PLAYLIST + "&key=" + API_KEY

vid_ids = []

print ("Retrieving video list...")

u = URL
while True:
    R = requests.get(u).json()
    for V in R["items"]:
        vid_ids.append((V["snippet"]["resourceId"]["videoId"], V["snippet"]["title"], V["snippet"].get("thumbnails", {"high":""})["high"]))
    if "nextPageToken" in R:
        u = URL + "&pageToken=" + R["nextPageToken"]
    else:
        break

print ("%d vids!" % len(vid_ids))

os.system("mkdir -p " + PLAYLIST_PATH)
os.system("mkdir -p " + PLAYLIST_PATH + "/m4a/")
os.system("rm -rf " + PLAYLIST_PATH + "/m4a/*")
os.system("mkdir -p " + PLAYLIST_PATH + "/mp3/")
os.system("rm -rf " + PLAYLIST_PATH + "/mp3/*")

def download_video(args):
    (vid, vname, thumb) = args

    url = "https://www.youtube.com/watch?v=" + str(vid)
    video = pafy.new(url)
    best_audio = video.getbestaudio(preftype="m4a")
    filename = os.path.join(PLAYLIST_PATH, vid) + "." + best_audio.extension
    thumb_filename = os.path.join(PLAYLIST_PATH, vid) + "-thumb.jpg"
    thumb_file_exists = False
    thumb_data = None
    try:
        with open(thumb_filename, "rb") as thumb_file:
            thumb_file_exists = True
            thumb_data = thumb_file.read()
    except: pass
    if not thumb_file_exists:
        R = requests.get(url=thumb["url"])
        with open(thumb_filename, "wb") as F:
            F.write(R.content)
        thumb_data = R.content

    file_exists = False
    try:
        with open(filename, "r"):
            file_exists = True
    except: pass
    if not file_exists:
        print ("Downloading {}".format(vname))
        best_audio.download(filepath=filename, quiet=True)

    (artists, song_name) = mazeeka_purifier.parse_song_title(vname)
    new_filename = os.path.join(PLAYLIST_PATH, "m4a", song_name + "." + best_audio.extension)
    with open(filename, "rb") as read_file:
        with open(new_filename, "wb") as write_file:
            write_file.write(read_file.read())
    mazeeka_purifier.fix_audio_file(new_filename, song_name, artists[0], thumb_data)

    return new_filename

def convert_video(filename):
    # convert m4a to mp3
    new_filename = filename.replace('m4a', 'mp3')

    # convert m4a to mp3
    os.system("ffmpeg -i \"{}\" -acodec libmp3lame -ab 128k \"{}\"".format(filename, new_filename))

p = Pool(16)
video_filenames = p.map(download_video, vid_ids)
print (video_filenames)
p.map(convert_video, video_filenames)
