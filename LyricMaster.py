# -*- coding: utf_8 -*-

# LYRICMASTER V1 BETA
# June 16, 2014


# TO DO:
#   - try/catch for changing directories
#   - surpress warnings
#   - Scrape nonMP3 songs
#   - Implement a 'similar to' search feature
#   - manual addition of lyrics and artists
#   - Remove all non unicode characters; Allow use with non-english titles


# Import all the things
import os
import time
import eyed3
import urllib
<<<<<<< HEAD
import warnings
=======
import fileinput
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.filedb.filestore import FileStorage
from whoosh.query import *
from whoosh.qparser import QueryParser

>>>>>>> dbc967c5078ecad27c904adb17a3d5ec150af50a

def startUp():
    '''
    startUp()
    Runs upon execution of LyricMaster.py; Contains the main menu
    INPUTS: (none)
    OUTPUTS: (none)
    '''
<<<<<<< HEAD
    
    warnings.filterwarnings('ignore')
    # Run from command line; Initate start up 
=======

    # Clear the terminal; allows for both windows and unix use
>>>>>>> dbc967c5078ecad27c904adb17a3d5ec150af50a
    os.system('cls' if os.name == 'nt' else 'clear')
    welcomeText = '''
    Welcome to LyricMaster
    V1 Beta; June 16, 2014\n\n
    '''
    origDir = os.getcwd();  # Save this so we can go back to it
    print welcomeText
    c = '';
    # Prompt the user for some action
    while c != 'q':
        os.chdir(origDir)   # Change directory back; useful for search
        print 'What would you like to do?'
        c =raw_input('Scrape Lyrics [L], Search [s], Quit [q] \t').lower()
        if c == 'q' or c == 'quit':
            print 'Thanks for using LyricMaster. We hope to see you soon! \n\n'
            break
        elif c == 'l' or c == 'lyrics' or c == 'scrape lyrics':
            print '\tFinding Lyrics'
            scrapeLyrics(origDir)
        elif c == 's' or c == 'search':
            print 'Alright. Lets do this\n'
            searchIndex()
        else:
            print 'I\'m sorry, I don\'t understand what you mean. Try again.'


def scrapeLyrics(origDir):
    '''
    scrapeLyrics(origDir)
    used to traverse the file system tree to gather song artists/titles
        then use the information to scrape lyrics from azlyrics.com
    Saves the results to a LyricsFile (text) that can be used for searching
    INPUTS: origDir -- starting directory; place to create index
    OUTPUTS: (none)
    '''

    # Find out if the user wants to start in the current directory
    # Will change current directory to be where user wants to start
    while True:
        q = 'Do you want to start a new Lyrics Index? [y/n]\t'
        c = raw_input(q).lower()
        if c == 'y' or c == 'yes':
            # Start a new file
            #LF = newLyricsFile() # Chaning to index
            idx = newIndex()
            break
        elif c == 'n' or c == 'no':
            # ask for the existing file
            print 'I\'m sory, this feature has not been implemented yet :('
        elif c == 'q' or c == 'quit':
            # Return to the main menu
            print '\tReturning to the Main Menu\n'
            return 
        else:
            print 'I\'m sorry, I don\'t understand what you mean. Try again.'

    # Find directory
    while True:
        q = 'Do you want to start in the current directory? [y/n]\t'
        cd = raw_input(q).lower()
        if cd == 'n' or cd == 'no':
            # Change to the directory we want
            while True:
                q = 'What directory do you want to start in?\t'
                dir = raw_input(q).decode()
                try:
                    os.chdir(dir)
                    break
                except WindowsError:
                    print 'Sorry, I couldn\'t navigate to that directory'
            break
        elif cd == 'y' or cd == 'yes':
            dir = os.getcwd().decode()
            break
        elif cd == 'q' or cd == 'quit':
            # Return to the main menu
            print '\tReturing to Main Menu\n'
            return
        else:
            print 'I\'m sorry, I don\'t understand what you mean. Try again.'
    print dir

    songsAndArtists = []    # Store mp3 data; [ (artist, title), ...]
    nonMP3 = [];            # For the non-mp3 files

    # Figure out all the songs we are dealing with
    for path, dirs, files in os.walk(dir):
        for name in files:
            root, ext = os.path.splitext(name)
            # mp3s can be proccessed with the eyed3 module
            if ext in ['.mp3']:
                #print name.encode('ascii')
                songPath = (os.path.join(path, name))   # Get filepath
                songPath = songPath.encode('ascii')
                print songPath
                #songPath = songPath.encode('ascii', 'ignore')
                print 'this is the path: ' + songPath
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
    #print songsAndArtists
    #print nonMP3

    # Scrape azlyrics; currently only does the artist/title combos 
    print '\nNOTE: LyricMaster currently only supports mp3 files'
    print 'All other music files will be ignored\n'

    os.chdir(origDir) 
    writer = idx.writer()
    for entry in songsAndArtists:
        # Scrape the lyrics and add them to the index
        addLyrics(entry[0], entry[1], writer)
    # Change directory back to original directory
    os.chdir(origDir) 
    writer.commit()      # commit and close the writer
    print '\nLyric Collection Complete\n\n'


def newIndex():
    '''
    initializeSearch()
    Creates the index/schema for the Whoosh module
    INPUTS: (none)
    OUTPUTS: idx -- index 
    '''
    print '\tCreating a new Index in the current directory'
    # Create an index to store the artist/title and lyrics
    schm = Schema(artistAndSong=KEYWORD(stored=True), lyrics=TEXT(stored=True))
    # Create a directory called LM_Storage; will contain the index
    # See Whoosh documentation for more information
    if not os.path.exists('LM_Storage'):
        os.mkdir('LM_Storage')
    idxDir ='LM_Storage'
    storage = FileStorage(idxDir)
    idx = storage.create_index(schm, indexname='LM')
    idx = storage.open_index(indexname = 'LM')
    return idx


def addLyrics(artist, title, writer):
    '''
    addLyrics(artist, title, writer)
    Used to scrape the lyrics; 
    replacement for getTheLyrics()
    INPUTS: artist -- artist of the track
            title -- title of the track
            writer -- writer for the index object
    '''
    # use azlyrics to get lyrics for the songs
    urlBase = 'http://www.azlyrics.com/lyrics/'
    a = artist.replace(' ', '').lower()
    title = title.replace('','').lower()
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

    l = html[start+24:end]
    l = l.replace('<br />', '')
    l = l.replace('</i>', '')
    l = l.replace('<i>', '')

    #print l
    at = a + ' ' + title
    writer.add_document(artistAndSong = at.decode(), lyrics = l.decode())


def searchIndex():
    '''
    searchindex()
    Performs the requested search through the index/schema
    INPUTS: idx -- desired index to search
    OUTPUTS: results -- results of the search
    '''
    # Navigate to the LM index directory
    c = ''
    while True:
        print 'The current directory is ' + os.getcwd()
        ques = 'Is the LM index (directory) in the current directory? [y/n]\t'
        c = raw_input(ques).lower()
        if c == 'y' or c == 'yes':
            idxDir = os.getcwd()
            break
        elif c == 'n' or c == 'no':
            while True:
                idxDir = raw_input('Where is it?\t').lower()
                try:
                    os.chdir(idxDir)
                    break
                except WindowsError:
                    print 'Sorry, I couldn\'t navigate to that directory'
            break
        elif c == 'q' or c == 'quit':
            print '\tReturning to the Main Menu'
            return
        else:
            print 'I\'m sorry, I don\'t understand what you mean. Try again.'

    # Open the index
    idxDir = idxDir + '/LM_Storage'
    storage = FileStorage(idxDir)
    idx = storage.open_index(indexname = 'LM')
    
    # Determine what the user wants to search for 
    c = ''
    while True:
        ques = 'What would you like to search? song/artist [s], lyrics [L]\t'
        c = raw_input(ques).lower()
        if c == 's' or c == 'song/artist' or c == 'song':
            searchForSong(idx)
            break
        elif c == 'l' or c == 'lyrics':
            searchForLyrics(idx)
            break
        elif c == 'q' or c == 'quit':
            print '\tReturning to the Main Menu'
            return 
        else:
            print 'I\'m sorry, I don\'t understand what you mean. Try again.'

def searchForSong(idx):
    '''
    searchForSong(idx)
    Searhces the given index for the specified artist/title
      Will not search Lyric text
    INPUTS: idx -- the index for searching
    OUTPUTS: (none)
    '''
    print '\tSearching Arist and Title data'
    # Get the query from the user
    q = 'Enter keywords, seperated by spaces\t'
    c = raw_input(q).lower()
    parser = QueryParser('artistAndSong', idx.schema)
    query = parser.parse(c.decode())
    # print query
    # Open a searcher() object and find the correct result
    with idx.searcher() as searcher:
        results = searcher.search(query)
        print 'I\'ve found ' + str(len(results)) + ' results\n'
        
        for i in range(0,len(results)):
            print str(i) + '. ' + results.fields(i)['artistAndSong']

        print   # Give some buffer space for readability

        while True:
            ques = 'Which number do you want to see the lyrics to?\t'
            c = raw_input(ques)
            if c == 'q' or c == 'quit':
                print '\tReturning to the Main Menu'
                return
            try:
                num = int(c)
                if not(num >= 0 and num < len(results)):
                    print 'Hm. It seems you didn\'t enter a valid nubmer. Try again'
                else:
                    break
            except ValueError:
                print 'Hm. It seems you didn\'t enter a valid nubmer. Try again'
        print '\n\n\n\n'
        print 'Displaying lyrics for: ' + results.fields(num)['artistAndSong']
        print results.fields(num)['lyrics']
        print '\n\n'
        # Return to the main menu

def searchForLyrics(idx):
    '''
    searchForLyrics(idx)
    Searches the given index in the lyrics field for the phrase
      Will not search artist/title
    INPUTS: idx -- the index for searching
    OUTPUTS: (none)
    '''
    # Search through song lyrics for the specified phrase
    print '\t Searching Lyrics'
    q = 'Enter your phrase for the lyric serach\t'
    c = raw_input(q).lower()
    parser = QueryParser('lyrics', idx.schema)
    query = parser.parse(c.decode())
    # print query
    # Open a searcher() object and find the correct result
    with idx.searcher() as searcher:
        results = searcher.search(query)
        print '\nI\'ve found ' + str(len(results)) + ' results\n'
        print 'Here are the songs with those lyrics'

        for i in range(0,len(results)):
            print str(i) + '. ' + results.fields(i)['artistAndSong']

        print   # Give some buffer space for readability
        while True:
            ques = 'Which number do you want to see the lyrics to?\t'
            c = raw_input(ques)
            if c == 'q' or c == 'quit':
                print '\tReturning to the Main Menu'
                return
            try:
                num = int(c)
                if not(num >= 0 and num < len(results)):
                    print 'Hm. It seems you didn\'t enter a valid nubmer. Try again'
                else:
                    break
            except ValueError:
                print 'Hm. It seems you didn\'t enter a valid nubmer. Try again'
        print '\n\n\n\n'
        print 'Displaying lyrics for: ' + results.fields(num)['artistAndSong']
        print results.fields(num)['lyrics']
        print '\n\n'
        # Return to the main menu

if __name__ == "__main__":
    '''
    When run from the command line, runs startUp()
    '''
    startUp()
