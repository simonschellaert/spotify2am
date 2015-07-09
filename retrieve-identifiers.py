import csv
import struct
import urllib.parse, urllib.request
import json
import signal
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--skip", dest="skip", default=0,
                  help="Amount of lines to skip from the input file")
parser.add_argument("-i",
                  dest="input_filename",
                  default="spotify.csv",
                  help="Input file (CSV)")
parser.add_argument("-o",
                  dest="output_filename",
                  default="itunes.csv",
                  help="Output file (CSV)")

args = parser.parse_args()


def retrieve_itunes_identifier(title, artist):
    headers = {
        "X-Apple-Store-Front" : "143446-10,32 ab:rSwnYxS0 t:music2",
        "X-Apple-Tz" : "7200" 
    }
    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=MusicPlayer&term=" + urllib.parse.quote(title)
    request = urllib.request.Request(url, None, headers)

    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        songs = [result for result in data["storePlatformData"]["lockup"]["results"].values() if result["kind"] == "song"]
        
        # Attempt to match by title & artist
        for song in songs: 
            if song["name"].lower() == title.lower() and (song["artistName"].lower() in artist.lower() or artist.lower() in song["artistName"].lower()):
                return song["id"]
        
        # Attempt to match by title if we didn't get a title & artist match
        for song in songs: 
            if song["name"].lower() == title.lower():
                return song["id"]

    except:
        # We don't do any fancy error handling.. Just return None if something went wrong
        return None


itunes_identifiers = []

output_file = open(args.output_filename, 'w', encoding='utf-8')

def signal_handler(signal, frame):
    output_file.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

i = 0
skip = int(args.skip)
with open(args.input_filename, encoding='utf-8') as playlist_file:
    playlist_reader = csv.reader(playlist_file)
    next(playlist_reader)

    for row in playlist_reader:
        title, artist = row[1], row[2]
        i += 1
        if i < skip:
            continue
        itunes_identifier = retrieve_itunes_identifier(title, artist)

        if itunes_identifier:
            itunes_identifiers.append(itunes_identifier)
            output_file.write(str(itunes_identifier) + "\n")
            print("{}. {} - {} => {}".format(i, title, artist, itunes_identifier))
        else:
            print("{}. {} - {} => Not Found".format(i, title, artist))
