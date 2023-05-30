import csv
import urllib.parse, urllib.request
import json

def get_itunes_id(title, artist, album):
    base_url = "https://itunes.apple.com/search?country=FR&media=music&entity=song&limit=5&term="
    try:
        url = base_url + urllib.parse.quote(title + " " + artist + " " + album)
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        
        if data['resultCount'] == 0:
            url = base_url + urllib.parse.quote(title + " " + artist)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode('utf-8'))
            
            if data['resultCount'] == 0:
                url = base_url + urllib.parse.quote(title + " " + album)
                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request)
                data = json.loads(response.read().decode('utf-8'))
                
                if data['resultCount'] == 0:
                    url = base_url + urllib.parse.quote(title)
                    request = urllib.request.Request(url)
                    response = urllib.request.urlopen(request)
                    data = json.loads(response.read().decode('utf-8'))
    except:
        return print("An error occured with the request.")
    
    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        
        for each in data['results']:
            #Trying to match with the exact track name, the artist name and the album name
            if each['trackName'].lower() == title.lower() and each['artistName'].lower() == artist.lower() and each['collectionName'].lower() == album.lower():
                return each['trackId']
        
        for each in data['results']:            
            #Trying to match with the exact track name and the artist name
            if each['trackName'].lower() == title.lower() and each['artistName'].lower() == artist.lower():
                return each['trackId']
            
        for each in data['results']:
            #Trying to match with the exact track name and the album name
            if each['trackName'].lower() == title.lower() and each['collectionName'].lower() == album.lower():
                return each['trackId']
            
        for each in data['results']:
            #Trying to match with the exact track name and the artist name, in the case artist name are different between Spotify and Apple Music
            if each['trackName'].lower() == title.lower() and (each["artistName"].lower() in artist.lower() or artist.lower() in each["artistName"].lower()):
                return each['trackId']
            
        for each in data['results']:
            #Trying to match with the exact track name and the album name, in the case album name are different between Spotify and Apple Music
            if each['trackName'].lower() == title.lower() and (each["collectionName"].lower() in album.lower() or album.lower() in each["collectionName"].lower()):
                return each['trackId']  
            
        for each in data['results']:
            #Trying to match with the exact track name
            if each['trackName'].lower() == title.lower():
                return each['trackId']
            
        for each in data['results']:
            #Trying to match with the track name, in the case track name are different between Spotify and Apple Music
            if title.lower() in each['trackName'] or each['trackName'].lower() in title.lower():
                return each['trackId']
            
    except:
        #The error is handled later in the code
        return None
    
am_id = []

with open('spotify.csv', encoding='utf-8') as f_raw:
    f = csv.reader(f_raw)
    next(f)
    for row in f:
        title, artist, album =  row[1], row[3], row[5]
        track_id = get_itunes_id(title, artist, album)
        if track_id:
            am_id.append(track_id)
            print(f'{title} - {artist} - {album} => {track_id}')
        else:
            print(f'{title} - {artist} - {album} => NOT FOUND')
            with open('noresult.txt', 'a+') as f:
                f.write(f'{title} - {artist} - {album} => NOT FOUND')
                f.write('\n')

with open('itunes.csv', 'w', encoding='utf-8') as output_file:
    for each_id in am_id:
        output_file.write(str(each_id) + "\n")
        
# Developped by @therealmarius on GitHub
# Based on the work of @simonschellaert on GitHub
# Github project page: https://github.com/therealmarius/Spotify-2-AppleMusic