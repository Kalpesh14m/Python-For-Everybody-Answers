"""
To get credit for this assignment, perform the instructions below and upload your SQLite3 database here:

(Must have a .sqlite suffix)
You do not need to export or convert the database - simply upload the .sqlite file that your program creates. See the example code for the use of the connect() statement.

Musical Track Database
This application will read an iTunes export file in XML and produce a properly normalized database with this structure:

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
If you run the program multiple times in testing or with different files, make sure to empty out the data before each run.

You can use this code as a starting point for your application: http://www.py4e.com/code3/tracks.zip. The ZIP file contains the Library.xml file to be used for this assignment. You can export your own tracks from iTunes and create a database, but for the database that you turn in for this assignment, only use the Library.xml data that is provided.

To grade this assignment, the program will run a query like this on your uploaded database and look for the data it expects to see:

SELECT Track.title, Artist.name, Album.title, Genre.name
    FROM Track JOIN Genre JOIN Album JOIN Artist
    ON Track.genre_id = Genre.ID and Track.album_id = Album.id
        AND Album.artist_id = Artist.id
    ORDER BY Artist.name LIMIT 3
The expected result of the modified query on your database is:
Select Language​▼
Track	Artist	Album	Genre
Chase the Ace	AC/DC	Who Made Who	Rock
D.T.	AC/DC	Who Made Who	Rock
For Those About To Rock (We Salute You)	AC/DC	Who Made Who	Rock
"""

import sqlite3
import xml.etree.ElementTree as ET


#Function that we'll use to find the content of a specific field.
def find_field(track, wanted_field):
    """This function gets two parameters: track, a dictionary containing all
    the XML tags of a certain song, and wanted_field, a string representing the
    title of the tag we want to obtain.
    It works by finding a key tag with the text {wanted_field}, and
    returning the content of the following tag. If wanted_field doesn't
    match any tag, it returns a False"""

    #Variable we'll use to indicate when we've found wanted_field
    found = False

    for tag in track:
        if not found:
            #Looking for the wanted field
            if(tag.tag == "key" and tag.text == wanted_field):
                found = True
        else:
            #After founding it, we return the content of the following
            #tag (the one with its value)
            return tag.text

    return False



#PART 1: PREPARING THE DATABASE
#Connecting to the file in which we want to store our db
conn = sqlite3.connect('tracks.sqlite')
cur = conn.cursor()

#Getting sure it is empty
#We can use "executescript" to execute several statements at the same time
cur.executescript("""
    DROP TABLE IF EXISTS Artist;
   
    DROP TABLE IF EXISTS Album; 
    DROP TABLE IF EXISTS Genre;
    DROP TABLE IF EXISTS Track
    """)

#Creating it
cur.executescript(''' CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);
CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')


#PART 2: INSERTING THE DATA
#Getting the data and parsing it
data_source = open("tracks/Library.xml")
data = data_source.read()
xml_data = ET.fromstring(data)

#Obtaining every tag with track data
tracks_data = xml_data.findall("dict/dict/dict")

#Getting the values of the fields we'll insert
for track in tracks_data:
    title = find_field(track, "Name")
    artist = find_field(track, "Artist")
    genre = find_field(track, "Genre")
    album = find_field(track, "Album")
    length = find_field(track, "Total Time")
    count = find_field(track, "Play Count")
    rating = find_field(track, "Rating")

    #Artist
    if (artist): #If it's a filled string, != False
        #If the value hasn't been introduced yet and exists, we'll insert it
        artist_statement = """INSERT INTO Artist(name) SELECT ? WHERE NOT EXISTS 
            (SELECT * FROM Artist WHERE name = ?)"""
        SQLparams = (artist, artist) #Params needed for completing the statement
        cur.execute(artist_statement, SQLparams)

    #Genre
    if (genre): #If it's a filled string, != False
        #If the value hasn't been introduced yet and exists, we'll insert it
        genre_statement = """INSERT INTO Genre(name) SELECT ? WHERE NOT EXISTS 
            (SELECT * FROM Genre WHERE name = ?)"""
        SQLparams = (genre, genre)
        cur.execute(genre_statement, SQLparams)

    #Album
    if (album): #If it's a filled string, != False
        #First of all, we'll get the artist id
        artistID_statement = "SELECT id from Artist WHERE name = ?"
        cur.execute(artistID_statement, (artist, ))
        #.fetchone() returns a one-element tuple, and we want its content
        artist_id = cur.fetchone()[0]


        #Now we're going to insert the data
        album_statement = """INSERT INTO Album(title, artist_id) 
            SELECT ?, ? WHERE NOT EXISTS (SELECT * FROM Album WHERE title = ?)"""
        SQLparams = (album, artist_id, album)
        cur.execute(album_statement, SQLparams)

    #Track
    if (title): #If it's a filled string, != False
        #Obtaining genre_id
        genreID_statement = "SELECT id from Genre WHERE name = ?"
        cur.execute(genreID_statement, (genre, ))
        try:
            genre_id = cur.fetchone()[0]
        except TypeError:
            genre_id = 0
        #Obtaining album_id
        albumID_statement = "SELECT id from Album WHERE title = ?"
        cur.execute(albumID_statement, (album, ))
        try:
            album_id = cur.fetchone()[0]
        except TypeError:
            album_id = 0

        #Inserting data
        track_statement = """INSERT INTO Track(title, album_id, genre_id, len,
            rating, count) SELECT ?, ?, ?, ?, ?, ?
                WHERE NOT EXISTS (SELECT * FROM Track WHERE title = ?)"""
        SQLparams = (title, album_id, genre_id, length, rating, count, title)
        cur.execute(track_statement, SQLparams)


conn.commit()
cur.close()
