LyricMaster, V1 Beta
21 July, 2014

Welcome to the LyricMaster readme! Thanks for stoping by.
LyricMaster is a Work in Progress, so please excuse the bugginess.

TABLE OF CONTENTS:
    I. About
    II. Usage
        A. Getting Lyrics
        B. Searching
    III. Index Object
    IV. Known Issues

I. ABOUT
    At this point you might be asking yourself: "What the heck is this thing?"
    Well, LyricMaster is a pet project I started in the Summer of 2014 as a way
    to learn more about the Python language. 

    Inspiration struck one day as I was trying to determine what song was stuck
    in my head. I knew the lyrics, even the artist, but not which one of the 
    many songs in my library I was stuck on. LyricMaster provides the user the 
    ability to search the lyrics to their music for key words and phrases, or
    simply look up the lyrics in general
    
    I realize that there are Internet-based versions of this same thing, but
    those require access to the Internet. Additionally, LyricMaster will narrow 
    the serach to only songs that exist in the user's library. This can be 
    particularly useful if the lyrics in question are common to a multitude of
    tracks.

    This project uses both the eyeD3 and Whoosh modules. eyeD3 allows for the
    extraction of meta data from the .mp3 files in question, while Whoosh 
    streamlines the creation of an index object and provides a platform for
    searching the index. Documentation can be found here:
        http://pythonhosted.org//Whoosh/index.html
        http://eyed3.nicfit.net/

    I hope you find LyricMaster helpful or simply amusing.
    Happy Mastering!
    https://github.com/AnastasiaShuler/LyricMaster

II. USAGE
    This section gives a general walkthrough for the procedural use of 
    LyricMaster. Most of the usage is self-explainitory, but this should relieve
    any confusion. Also note that entering "q" at most menus (minus the two
    search query prompts) will return you to the main menu.
    
    A. Getting Lyrics
        Getting lyrics is easy! When LyricMaster is first run from the command
        line, you will be presented with a screen much like this:

                    Welcome to LyricMaster
                    V1 Beta; June 16, 2014

                What would you like to do?
                Scrape Lyrics [L], Search [s], Quit [q]

        Since we want to scrape lyrics, we're going to go ahead and enter the 
        character "L", followed by a return. This brings us to the following 
        prompt:

                    Finding Lyrics
                Do you want to start a new Lyrics Index? [y/n]

        As instructed, enter "y" or "n" depending on your desire to create a new
        Index. For more information about the index object, head over to the
        INDEX section.

        As using an existing Lyrics Index has not been implemented (it's a work
        in progress, okay?), lets go ahead and enter "y". Up comes this:

                    Creating a new Index in the current director
                Do you want to start in the current directory? [y/n]

        LyricMaster has successfully created a new folder in your current
        working directory to store all of the index stuff. Wee! The next choice
        we have to make is where to start the file tree traversal. If the 
        LyricMaster.py file has been placed in your "Music" folder, go ahead
        and hit "y" followed by return. Otherwise, type the full name of the
        directory you want to use instead. For instance, on a Windoze machine:

            c:/users/You/Music
            *NOTE: for Windoze, use the forward slash; the back slash 
                   will cause python to try and escape the next character

        Now we wait; LyricMaster will traverse the file tree in a top-to-bottom 
        mannar and collect all the music files it finds along the way. Once 
        the traversal is complete, it will search the Internet to find lyrics 
        to your music. Once complete, LyricMaster will return to the main menu.


    B. Searching
        Now that we have a Lyrics Index (either from a fresh traversal or from
        a slightly older scraping), we can search the collection. The main menu
        gives the following prompt:

                What would you like to do?
                Scrape Lyrics [L], Search [s], Quit [q]

        Choose Search by entering "s" followed by return. The following prompt 
        will be displayed:

                The current directory is C:\Users\currentWorkingDirectory
                Is the LM index (directory) in the current directory? [y/n]

        Here, we want to chose the directory that contains the LM_Storage 
        folder, not the file path of the folder itself. I know, confusing. 
        Either by hitting "y" or by entering "n" followed by the correct path, 
        we get ourselves to the next prompt:

            What would you like to search? song/artist [s], lyrics [L]

        We can either search by song/artist pairings or by searching the lyrics
        directly.

        i. Song/Artist pairs
            Enter this mode by simply hiting "s" followed by return. We meet the
            following prompt:

                        Searching Arist and Title data
                Enter keywords, seperated by spaces

            Do just that; enter the song title, the artist, or any combination 
            of the two. LyricMaster searches Song/Aritst data using keywords, so
            just be sure to seperate with spaces. Provided that something in
            the index matches your search, results will appear as shown:

                I've found 2 results
                
                0. Artist Song Title
                1. Artist Second Song Title
                
                Which number do you want to see the lyrics to?

            To get the lyrics for a track, enter the result number (the nubmer 
            to the left of the result). LyricMaster will display the lyrics 
            and return to the main menu. 

        ii. Lyrics
            To search lyrics, hit "L" and continue to the following prompt:

                    Searching Lyrics
                Enter your phrase for the lyric serach
           
            LyricMaster supports phrase searching for lyric data (but not for the
            song/artist data), so whatever you enter must be matched EXACTLY in
            one or more of the saved lyric stets. (In a future release,
            LyricMaster will support searching for 'similar' phrases). After 
            processing your query, we are faced with:
        
                I've found 1 results
                Here are the songs with those lyrics

                0. Artist Song Title
                
                Which number do you want to see the lyrics to?
           
           Just as in the Song/Artist search, enter the corresponding number to
           view the complete set of lyrics.


    More features are in the pipeline; Some include:
        - results that are 'similar' to your search query
        - some simple spelling/error correction based on data in index
        - document highlighting showing phrases matched in context
            (kinda like a Google search)


III. INDEX OBJECT
    LyricMaster utilizes the Whoosh module and the associated index object to 
    store scraped information (http://pythonhosted.org//Whoosh/index.html). 
    This allows for rapid searching, as well as long-term storage for the 
    gathered lyrics.

    The Lyrics Index is created with a Schema that stores two fields. It was 
    constructed as follows:

        Schema(artistAndSong=KEYWORD(stored=True), lyrics=TEXT(stored=True))

    This creates a schema with fields titled artistAndSong and lyrics. The field
    types are Keyword and Text respectively. The Keyword field type allows all
    words in the artistAndSong combination to be searched independantly. This,
    however, does not allow for phrase searching of these items. The Text field
    type for the lyrics gives the option of phrase searching in the lyrics
    field, which is far more usefull than treating the entire lyrics text as a
    collection of key words.

    Both fields are stored as well as indexed (as can be gathered by the 
    stored = True assignment). This allows the user to access the stored data,
    namely the lyrics, after performing the search. Storing the text, while it
    does take more space, should allow for the highlighted search result 
    exerpts that are a future feature.
    
    The Lyrics Index itself is stored in a directory called LM_Storage that is
    created by LyricMaster in the same directory as the .py file. Whoosh takes
    care of all the inside stuff. This folder can be specified to allow searches
    in the specified index. LyricMaster does not currently support more than one
    Lyrics Index (since it will always overwrite the one that exists in the
    current directory).


IV. KNOWN ISSUES
    Yea, I know about these ones. I'm working on fixing them, but for now just
    ignore them the best you can.

        - Cannot use existing Lyrics Index when scraping lyrics
        - Breaks when special characters are in the filenames
        - Song/Artist combinations lack casing and punctuation
            (I had a hard time making the index object store these; I didn't
             want to mess with it further)
        - Breaks if an invalid directory path is entered
        - Does occasionaly display warnings from eyeD3 module
        - Doesn't do anything with the non-mp3 files
        - white space in commands causes issues
