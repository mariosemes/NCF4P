# Welcome to NCF4P aka New Content Finder 4 Plex!

The idea behind this script was to have the ability to scroll trough Movies and TV Shows that are not already in your PLEX library, something like NETFLIX and other similar services offer.

## How it works.

The script is written in Python 3 and I didn't tested it with lower versions (maybe few minimum changes would make it work anyway). Everytime you trigger the script, it will ping TheMovieDB trough their API and get the most popular Movies and TV Shows right now. After getting the mentioned list of popular content, it will create Plex optimized folders and download its Trailer from YouTube with YouTube-DL. This way, you can create a separate Library on your Plex account that will only show Trailers.

![example](https://github.com/mariosemes/NCF4P/blob/master/Images/example.jpg?raw=true)

## Requirements

1. Python 3+
2. requests>=2.24.0 (install with pip)
3. youtube-dl>=2020.6.16.1 or higher (install with pip)
4. TheMovieDB API

## Settings.ini file

The settings.ini file contains all the settings that the script needs to work without troubles.
1. Create folder for "trailers"
2. Inside of "trailers" folder, create folder "movies"
3. Inside of "trailers" folder, create folder "tvshows"
4. Open up settings.ini file and put the full path to the created folders
5. Register a account on TheMovieDB and request an API (Google it or whatever...)

***Settings.ini file***
```
[tmdb]
API_KEY = TheMovieDB API key
LANGUAGE = example: en-US
PAGE_NO = Number of pages to go trough, example: 50

[date]
AGE_YEAR = Year of release, everything above it will be added. Example: 2019

[location]
MOVIE_LOCATION = D:\fake\movies
TV_LOCATION = D:\fake\tvshows
```

## Don't FORGET!!!

Just please, don't forget to add the new libraries into Plex. Name them something like "Movie Trailers" or "TV Show Trailers".


### Feel free to pull the script, fix, add, brake, I don't know whatever you want to do with it :)
Let me know and push it if you make something great.