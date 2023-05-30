import csv
import struct
import urllib.parse, urllib.request
import json

def get_itunes_id(title, artist, album):
    base_url = "https://itunes.apple.com/search?country=FR&media=music&entity=song&limit=5&term="
    url = base_url + urllib.parse.quote(title + " " + artist)
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        
        for each in data['results']:
            
            #Trying to match with the exact track name, the artist name and the album name
            if each['trackName'].lower() == title.lower() and each['artistName'].lower() == artist.lower() and each['collectionName'].lower() == album.lower():
                return each['trackId']
            
            #Trying to match with the exact track name and the artist name
            elif each['trackName'].lower() == title.lower() and each['artistName'].lower() == artist.lower():
                return each['trackId']
            
            #Trying to match with the exact track name and the album name
            elif each['trackName'].lower() == title.lower() and each['collectionName'].lower() == album.lower():
                return each['trackId']
            
            #Trying to match with the exact track name and the artist name, in the case artist name are different between Spotify and Apple Music
            elif each['trackName'].lower() == title.lower() and (each["artistName"].lower() in artist.lower() or artist.lower() in each["artistName"].lower()):
                return each['trackId']
            
            #Trying to match with the exact track name and the album name, in the case album name are different between Spotify and Apple Music
            elif each['trackName'].lower() == title.lower() and (each["collectionName"].lower() in album.lower() or album.lower() in each["collectionName"].lower()):
                return each['trackId']  
            
            #Trying to match with the exact track name
            elif each['trackName'].lower() == title.lower():
                return each['trackId']
            
            #Trying to match with the track name, in the case track name are different between Spotify and Apple Music
            elif title.lower() in each['trackName'] or each['trackName'].lower() in title.lower():
                return each['trackId']
            
            # If no match, return the first result
            else:
                return print(f'No result for {title} - {artist} - {album}')
            
    except:
        return None
            
 


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


with open('spotify.csv', encoding='utf-8') as playlist_file:
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
            noresult = "{} - {} => Not Found".format(title, artist)
            with open('noresult.txt', 'a+') as f:
                f.write(noresult)
                f.write('\n')


with open('itunes.csv', 'w', encoding='utf-8') as output_file:
    for itunes_identifier in itunes_identifiers:
        output_file.write(str(itunes_identifier) + "\n")


# Developped by @therealmarius on GitHub
# Based on the work of @simonschellaert on GitHub
# Github project page: https://github.com/therealmarius/Spotify-2-AppleMusic