# LYRICMASTER V1 BETA
# June 14, 2014

# Import all the things

# TO DO:
#   - try/catch for changing directories
#   - surpress warnings
#   - Implement the feature to utlize a previous lyrics file


import os
import time
import eyed3
import urllib
import fileinput

def startUp():
    '''
    startUp()
    Runs upon execution of LyricMaster.py; Contains the main menu
    Inputs: (none)
    Outputs: (none)
    '''

    # Run from command line; Initate start up 
    # Clear the terminal; allows for both windows and unix use
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
    '''
    scrapeLyrics()
    used to traverse the file system tree to gather song artists/titles
        then use the information to scrape lyrics from azlyrics.com
    Saves the results to a LyricsFile (text) that can be used for searching
    Inputs: (none)
    Outputs: (none)
    '''

    # Find out if the user wants to start in the current directory
    # Will change current directory to be where user wants to start
    while True:
        q = 'Do you want to start a new Lyrics file? [y/n]\t'
        c = raw_input(q).lower()
        if c == 'y' or c == 'yes':
            # Start a new file
            LF = newLyricsFile()
            break
        elif c == 'n' or c == 'no':
            # ask for the existing file
            print 'I\'m sory, this feature has not been implemented yet :('
        else:
            print 'I\'m sorry, I don\'t understand what you mean. Try again.'

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
    added = [];             # To keep track of which songs have been added to LF

    for path, dirs, files in os.walk(dir):
        for name in files:
            root, ext = os.path.splitext(name)
            # mp3s can be proccessed with the eyed3 module
            if ext in ['.mp3']:
                songPath = os.path.join(path, name) # Get filepath
                sFile = eyed3.load(songPath)
                # try/catch to avoid throwing AttributeError
                try:
                    # use eyed3 module to get meta data
                    sArtist = sFile.tag.artist
                    sTitle = sFile.tag.title
                    songsAndArtists.append((sArtist,sTitle))
                except AttributeError:
                    # remove any sort of odd characters from filename
                    root = root.replace('.', ' ')
                    root = root.replace('_', ' ')
                    nonMP3.append(root)
                    print 'This .mp3 doesn\'t seem to have meta data'
            elif ext in ['.m4a', '.m4p', '.wav', '.wma']: 
                root = root.replace('.', ' ')
                root = root.replace('_', ' ')
                nonMP3.append(root)
    # Give some new lines in here to make it a little easier to read
    print
    print
    print
    print songsAndArtists
    print nonMP3
    allFiles = songsAndArtists + nonMP3
    LF.write(str(allFiles) + '\n\n');    # Make this the first line in the LF
    LF.write('\n\n')
    # Will need to change this; can't include files that have no lyrics

    # Scrape azlyrics; currently only does the artist/title combos 
    for entry in songsAndArtists:
        getTheLyrics(entry[0], entry[1], LF, added)

    # This doesn't work
    #LF.seek(0)
    #LF.write(str(added))

    print 'Lyric Collection Complete\n\n'
    # Closes the lyric file; Will eventually be moved
    LF.close()


def newLyricsFile():
    '''
    newLyricsfile()
    Initiates a new text file to store the lyrics
    Gives the option to use the default name or a personalized filename
    Inputs: (none)
    Outputs: file Object
    '''
    while True:
        c = raw_input('Use the default file Name?\t').lower()
        if c == 'y' or c == 'yes':
            # make file with the defualt name
            fileName = 'LMLF' + '_' + time.strftime('%d-%m-%Y')
            break
        elif c == 'n' or c == 'no':
            # ask for their own file name
            fileName = raw_input('What would you like to call it?\t')
            break
        else:
            print 'I\'m sorry, I don\'t understand what you mean. Try again.'
    fileName = fileName + '.txt'
    print 'Created new LyricFile called ' + fileName
    return open(fileName, 'w')


def getTheLyrics(artist, title, LF, added):
    '''
    getTheLyrics(artist, title)
    Uses azlyrics.com to get lyrics for the known artist/title pairs
    Inputs: artist -- artist of the track
            title -- title of the track
            lyricFile -- text file to store lyrics in
            added -- list containing all the artists/songs added to the file
    Outputs: lyrics -- string containing the lyrics of the track
    '''
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
    if start == -1 or end == -1:
        #There's no lyrics for this combination
        return

    lyrics = html[start+24:end]
    lyrics = lyrics.replace('<br />', '')
    lyrics = lyrics.replace('\n', ' ')   # Remove all of the new lines

    lyrics = artist + ', ' + title + ': ' + lyrics + '\n'
    print lyrics
    LF.write(lyrics)
    added.append((artist,title))


if __name__ == "__main__":
    '''
    When run from the command line, runs startUp()
    '''
    startUp()
