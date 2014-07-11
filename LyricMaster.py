# LYRICMASTER V1 BETA
# June 10, 2014

# Import all the things

# TO DO:
#   - try/catch for changing directories
#   - surpress warnings


import os
import eyed3
import urllib

def startUp():
    # Run from command line; Initate start up 
    os.system('cls' if os.name == 'nt' else 'clear')
    welcomeText = '''
    Welcome to LyricMaster
    V1 Beta; June 10, 2014\n\n
    What would you like to do?
    '''
    print welcomeText
    c = '';
    # Prompt the user for some action
    while c != 'q':
        c =raw_input('Scrape Lyrics [L], Search [s], Quit [q] \t').lower()
        if c == 'q' or c == 'quit':
            print 'Thanks for using LyricMaster. We hope to see you soon! \n\n'
        elif c == 'l' or c == 'lyrics' or c == 'scrape lyrics':
            print 'Finding Lyrics'
            scrapeLyrics()
        elif c == 's' or c == 'search':
            print 'Alright. Lets do this'
        else:
            print 'I\'m sorry, I don\'t understand what you mean. Try again.'

def scrapeLyrics():
    # Find out if the user wants to start in the current directory
    # Will change current directory to be where user wants to start
    while True:
        q = 'Do you want to start in the current directory? [y/n]\t'
        cd = raw_input(q).lower()
        if cd == 'n' or cd == 'no':
            # Change to the directory we want
            dir = raw_input('What directory do you want to start in?\t')
            os.chdir(dir)
            break
        elif cd == 'y' or cd == 'yes':
            dir = os.getcwd()
            break
        else:
            print 'I\'m sorry, I don\'t understand what you mean. Try again.'
    print dir

    songsAndArtists = []    # Store mp3 data; [ (artist, title), ...]
    nonMP3 = [];            # For the non-mp3 files

    for path, dirs, files in os.walk(dir):
        for name in files:
            root, ext = os.path.splitext(name)
            # mp3s can be proccessed with the eyed3 module
            if ext in ['.mp3']:
                songPath = os.path.join(path, name)
                sFile = eyed3.load(songPath)
                # Want to make sure this doesn't break if the .mp3 doesn't have shit
                try:
                    sArtist = sFile.tag.artist
                    sTitle = sFile.tag.title
                    songsAndArtists.append((sArtist,sTitle))
                except AttributeError:
                    root = root.replace('.', ' ')
                    root = root.replace('_', ' ')
                    nonMP3.append(root)
                    print 'This .mp3 doesn\'t seem to have meta data'
            elif ext in ['.m4a', '.m4p', '.wav', '.wma']: 
                root = root.replace('.', ' ')
                root = root.replace('_', ' ')
                nonMP3.append(root)
    print
    print
    print
    print songsAndArtists
    print nonMP3
    for entry in songsAndArtists:
        getTheLyrics(entry[0], entry[1])

def getTheLyrics(artist, title):
    # use azlyrics to get lyrics for the songs
    urlBase = 'http://www.azlyrics.com/lyrics/'
    artist = artist.replace(' ', '').lower()
    title = title.replace(' ','').lower()
    url = urlBase + artist + '/' + title +'.html'
    print url
    
    html = urllib.urlopen(url)   # Gives HTML for the webpage
    html = html.read()
    start = html.find('<!-- start of lyrics -->')
    end = html.find('<!-- end of lyrics -->')
    lyrics = html[start+24:end]
    lyrics = lyrics.replace('<br />', '')
    print lyrics

if __name__ == "__main__":
    startUp()
