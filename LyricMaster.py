# LYRICMASTER V1 BETA
# June 14, 2014

# Import all the things

# TO DO:
#   - try/catch for changing directories
#   - surpress warnings
#   - Implement the feature to utlize a previous lyrics file
#   - Scrape nonMP3 songs
#   - Implement search feature


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
    V1 Beta; June 14, 2014\n\n
    '''
    print welcomeText
    c = '';
    # Prompt the user for some action
    print 'What would you like to do?'
    while c != 'q':
        c =raw_input('Scrape Lyrics [L], Search [s], Quit [q] \t').lower()
        if c == 'q' or c == 'quit':
            print 'Thanks for using LyricMaster. We hope to see you soon! \n\n'
        elif c == 'l' or c == 'lyrics' or c == 'scrape lyrics':
            print '\tFinding Lyrics'
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
        q = 'Do you want to start a new Lyrics Index? [y/n]\t'
        c = raw_input(q).lower()
        if c == 'y' or c == 'yes':
            # Start a new file
            #LF = newLyricsFile() # Chaning to index
            newIndex()
            break
        elif c == 'n' or c == 'no':
            # ask for the existing file
            print 'I\'m sory, this feature has not been implemented yet :('
        else:
            print 'I\'m sorry, I don\'t understand what you mean. Try again.'
    # Find directory
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

    # Figure out all the songs we are dealing with
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
    #print songsAndArtists
    #print nonMP3
    allFiles = songsAndArtists + nonMP3
    # Use a temporary file to store all lyrics in;
    # Allows for the first line to be the stored artist/titles
    temp = open('LM_temp.txt', 'w')
    # Will need to change this; can't include files that have no lyrics

    # Scrape azlyrics; currently only does the artist/title combos 
    print '\nNOTE: LyricMaster currently only supports mp3 files'
    print 'All other music files will be ignored\n'

    for entry in songsAndArtists:
        getTheLyrics(entry[0], entry[1], temp, added)
    temp.close()
    temp = open('LM_temp.txt', 'r')
    # Make sure the list of contained songs is the first line
    LF.write(str(added) + '\n\n')
    for line in temp:
        LF.write(line)
    print '\nLyric Collection Complete\n\n'

    # Closes the lyric file; Will eventually be moved
    temp.close()
    os.remove('LM_temp.txt')
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
        c = raw_input('\tUse the default file Name?\t').lower()
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
    print '\tCreated new LyricFile called ' + fileName
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
    a = artist.replace(' ', '').lower()
    t = title.replace(' ','').lower()
    url = urlBase + a + '/' + t +'.html'
    #print url
    
    html = urllib.urlopen(url)   # Gives HTML for the webpage
    html = html.read()
    start = html.find('<!-- start of lyrics -->')
    end = html.find('<!-- end of lyrics -->')
    if start == -1 or end == -1:
        #There's no lyrics for this combination
        print '\tWhoops. Could not find any lyrics for ' + artist +'/' + title
        return

    lyrics = html[start+24:end]
    lyrics = lyrics.replace('<br />', '')
    lyrics = lyrics.replace('\n', ' ')   # Remove all of the new lines
    #print lyrics
    lyrics = artist + ', ' + title + ': ' + lyrics + '\n'
    LF.write(lyrics)
    added.append((artist,title))

def newIndex()
    '''
    initializeSearch()
    Creates the index/schema for the Whoosh module
    INPUTS: (none)
    OUTPUTS: idx -- index 
    '''
    # Want to allow lyric search and artist/title search
    from whoosh.fields import Schema, TEXT, KEYWORD
    from whoosh.index import create_in

    print 'Creating a new Index'
    # Create an index to store the artist/title and lyrics
    schm = Schema(artistAndSong=KEYWORD(stored=True), lyrics = TEXT(stored=True)
    index = 'LM_Storage'
    if not os.path.exists('LM_Storage')
        os.mkdir('LM_Storage')
    idx = create_in('LM_Storage', schm)
    idx = open_dir('LM_Storage')
    return idx

def lyrics(artist, title, writer)
    '''
    lyrics(artist, title, idx)
    Used to scrape the lyrics; replacement for getTheLyrics()
    INPUTS: artist -- artist of the track
            title -- title of the track
            writer -- writer for the index object
    '''
    # use azlyrics to get lyrics for the songs
    urlBase = 'http://www.azlyrics.com/lyrics/'
    a = artist.replace(' ', '').lower()
    t = title.replace(' ','').lower()
    url = urlBase + a + '/' + t +'.html'
    #print url
    
    html = urllib.urlopen(url)   # Gives HTML for the webpage
    html = html.read()
    start = html.find('<!-- start of lyrics -->')
    end = html.find('<!-- end of lyrics -->')
    if start == -1 or end == -1:
        #There's no lyrics for this combination
        print '\tWhoops. Could not find any lyrics for ' + artist +'/' + title
        return

    lyrics = html[start+24:end]
    lyrics = lyrics.replace('<br />', '')
    lyrics = lyrics.replace('\n', ' ')   # Remove all of the new lines
    #print lyrics
    writer.add
    wtr.add_document(artistAndSong = u'this is a big test', lyrics= u'SOME FANCY SHIT')


def searchIndex(idx)
    '''
    searchindex()
    Performs the requested search through the index/schema
    INPUTS: idx -- desired index to search
    OUTPUTS: results -- results of the search
    '''
    pass

if __name__ == "__main__":
    '''
    When run from the command line, runs startUp()
    '''
    startUp()
