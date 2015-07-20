import csv
import struct
import urllib.parse, urllib.request
import json
import time
from difflib import SequenceMatcher

DEBUG = 0  # Set to 1 for closer inspection

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def retrieve_itunes_identifier(title, artist):
    headers = {
        "X-Apple-Store-Front" : "143446-10,32 ab:rSwnYxS0 t:music2",
        "X-Apple-Tz" : "7200" 
    }
    
    search_string = str(artist) +" " + str(title)
    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=MusicPlayer&term=" + urllib.parse.quote(search_string)
    request = urllib.request.Request(url, None, headers)

    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        songs = [result for result in data["storePlatformData"]["lockup"]["results"].values() if result["kind"] == "song"]
        
        
        # Attempt to match by title & artist
        for song in songs:
            
            song_match = similar(song["name"].lower() , title.lower())
            artist_match = similar(song["artistName"].lower() , artist.lower())
            
            if DEBUG == 1:
                
                print ("Requested:",artist, " : ",title," => Received:",song["artistName"]," : " ,song["name"])
                print ("Confidence : Artist " + str(round(artist_match*100)),"%  Song " + str(round(song_match*100)) + "%")
                input("Press Enter to continue...")            
            
            
            # For primary matches, lets assume that artist string should always match
            if song["artistName"].lower() == artist.lower():
                if (song["name"].lower() in title.lower()):               
                    return (song["id"],'Primary')
            
                # Attempt to match by title if we didn't get an exact title & artist match
                # For secondary matches, lets assume that artist string should always match
                # return if song title similarty > 80%
             
            elif song["artistName"].lower() == artist.lower():
                if song_match > 0.7:
                    return (song["id"],'Secondary')
                       
            elif artist_match > 0.8:
                if song_match > 0.7:
                    return (song["id"],'Fuzzy')
                
            else:
                print("FAIL: Could not find suitable match for: {} - {}".format(artist, title))
                return None

    except KeyError as e:
        print("FAIL: Nothing returned for: {} - {}".format(artist, title))
        #We don't do any fancy error handling.. Just return None if something went wrong
        return None



itunes_identifiers = []


with open('spotify.csv', encoding='utf-8') as playlist_file:
    playlist_reader = csv.reader(playlist_file)
    next(playlist_reader)

    for row in playlist_reader:
        title, artist = row[1], row[2]
        itunes_identifier = retrieve_itunes_identifier(title, artist)

        if itunes_identifier:
            if itunes_identifier[1] == 'Primary':
                itunes_identifiers.append(itunes_identifier)
                print("SUCCESS: Exact match: {} - {} => {}".format(title, artist, itunes_identifier[0]))
            
            elif itunes_identifier[1] == 'Secondary':
                itunes_identifiers.append(itunes_identifier)
                print("SUCCESS: Secondary match: {} - {} => {}".format(title, artist, itunes_identifier[0]))
                
            elif itunes_identifier[1] == 'Fuzzy':
                itunes_identifiers.append(itunes_identifier)
                print("SUCCESS: Fuzzy match: {} - {} => {}".format(title, artist, itunes_identifier[0]))
        else:
            pass


with open('itunes.csv', 'w', encoding='utf-8') as output_file:
    for itunes_identifier in itunes_identifiers:
        output_file.write(str(itunes_identifier[0]) + "\n")
