import csv
import struct
import urllib.parse, urllib.request
import json


def retrieve_itunes_identifier(title, artist):
    headers = {
        "X-Apple-Store-Front" : "143446-10,32 ab:rSwnYxS0 t:music2",
        "X-Apple-Tz" : "7200" 
    }
    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=MusicPlayer&term=" + urllib.parse.quote(title)
    request = urllib.request.Request(url, None, headers)

    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.readall().decode('utf-8'))
        
        for result in data["storePlatformData"]["lockup"]["results"].values():
            if result["kind"] == "song" and result["name"].lower() == title.lower() and (result["artistName"].lower() in artist.lower() or artist.lower() in result["artistName"].lower()):
                return result["id"]
    except:
        return None


itunes_identifiers = []


with open('spotify.csv') as playlist_file:
    playlist_reader = csv.reader(playlist_file)
    next(playlist_reader)

    for row in playlist_reader:
        title, artist = row[1], row[2]
        itunes_identifier = retrieve_itunes_identifier(title, artist)

        if itunes_identifier:
            itunes_identifiers.append(itunes_identifier)
            print("{} - {} => {}".format(title, artist, itunes_identifier))
        else:
            print("{} - {} => Not Found".format(title, artist))


with open('itunes.csv', 'w') as output_file:
    for itunes_identifier in itunes_identifiers:
        output_file.write(str(itunes_identifier) + "\n")
