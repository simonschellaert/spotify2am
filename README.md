# Spotify to Apple Music
## Based on the work of [@simonschellaert](https://github.com/simonschellaert/spotify2am)
Some simple Python 3 scripts to help you into importing your existing Spotify playlists into Apple Music.  

## Usage

### 1. Export the Spotify songs to a CSV File
The first step is getting the songs you want to import into Apple Music into a CSV file. The simplest way to do this is using [Exportify](https://watsonbox.github.io/exportify/).  
If you want to export you whole Spotify library, simply create a new playlist called **All** and drag your whole library into it using the Spotify desktop app. You can then export the playlist **All** using **Exportify**. Save the resulting file as **spotify.csv** in the same directory as the directory you cloned this repo into.

### 2. Match the Spotify songs with their Apple Music identifier
In order to add songs to our Apple Music playlist, we need their Apple Music identifier. Running `python3 retrieveIdentifiers.py` will use the **spotify.csv** file to create a new file **itunes.csv** with each line consisting of the Apple Music identifier of a song in your Spotify playlist.
And now, all songs that haven't match any Apple Music identifiers are added to a **noresult.txt** file.

### 3. Open Apple Music in Firefox
* To add our songs to the playlist we want, you'll need to open [Apple Music](https://music.apple.com/login) into [Firefox](https://www.mozilla.org/firefox/new/) (I use Firefox but you can try to do the same on other browser. But it works for me using Firefox. You'll maybe have to adapt the following steps).
* When you're logged in open the **Dev Tools** (**Ctrl + Shift + I** or **F12** on Windows and Linux or **Cmd + Opt + I** on macOS). 
* Then, go the **Network** tab and add a random song to the playlist where you want your Spotify songs. (Using the Apple Music web interface).
* Look for a POST request to a url like this: `https://amp-api.music.apple.com/v1/me/library/playlists/p.ID/tracks` (`p.ID` stands; of course, for the unique playlist ID. So, don't search for the exact same url! You won't find it.)
* When you find it, click on it and go to the **Headers** tab.
* Then, hit the Resend button. It should be on the top right of the **Headers** tab.
* Here come the tricky part... Hold on, you can do it. Open a terminal and run `python3`. Then, quickly import [pyautogui](https://pypi.org/project/PyAutoGUI/). (Make sure you have it installed before)
* Back in our browser, in the **Resend request** tab, you should see the payload of the request. Remove the song id (your payload should look like this: {"data":[{"id":"","type":"songs"}]} Please check because this step is important), and put your cursor right beetwen the 2 dobule quotes.
* In the terminal, run `pyautogui.position()`. It should return a tuple with two numbers. Replace the numbers in the line 14 and in the line 17 with the numbers you got from the terminal.
* Then, in your browser, put your cursor above the send button, and run the same command in the terminal. Replace the numbers in the line 19 with the numbers you got from the terminal.

Now you should be ready to go. Run the following:
```bash
python3 insertSongs.py
```

When the script runs, just select your browser window and wait for the magic to happen.

## Limitations

### Missing songs
The script I'm using to retrieve the Apple Music identifier for a Spotify song is quite basic. It simply compares the title and artist to find out if a Spotify and Apple Music song match. Some songs don't have the exact same title (extraneous spacing for example) in both services. This results in the script failing to retrieve an identifier for some songs. Hopefully, you'll be able to add the missing songs manually thanks to the **noresult.txt** file.
