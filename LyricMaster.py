# LYRICMASTER V1 BETA
# June 10, 2014

# Import all the things

# TO DO:
#   - try/catch for changing directories
#   - surpress warnings


import os
import eyed3

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
    songsAndArtists = [] # List to store the files in
    # Testing the os.walk funciton
    for path, dirs, files in os.walk(dir):
        for name in files:
            root, ext = os.path.splitext(name)
            if ext in ['.mp3']:
                songPath = os.path.join(path, name)
                sFile = eyed3.load(songPath)
                # Want to make sure this doesn't break if the .mp3 doesn't have shit
                try:
                    sArtist = sFile.tag.artist
                    sTitle = sFile.tag.title
                    songsAndArtists.append((sArtist,sTitle))
                except AttributeError:
                    print 'This .mp3 doesn\'t seem to have meta data'
    print songsAndArtists

#        for name in files:
#            # Add the music files to a list
#            root, ext = os.path.splitext(name)
#            if ext in ['.mp3', '.m4a', '.m4p', '.wav', '.wma']: 
#                root = root.replace('.', ' ')
#                root = root.replace('_', ' ')
#                musicFiles.append(root)
#    print musicFiles



if __name__ == "__main__":
    startUp()
