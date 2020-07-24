from __future__ import unicode_literals
import datetime
import os
import requests
from requests.exceptions import HTTPError
import youtube_dl
import configparser


class MyParser(configparser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


# Editable content ######################################################

f = MyParser()
f.read("settings.ini")
settings_file = f.as_dict()


API_KEY = settings_file["tmdb"]["api_key"]
LANGUAGE = settings_file["tmdb"]["language"]
PAGE_NO = settings_file["tmdb"]["page_no"]
AGE_YEAR = settings_file["date"]["age_year"]
MOVIE_LOCATION = settings_file["location"]["movie_location"]
TV_LOCATION = settings_file["location"]["tv_location"]

now = datetime.datetime.now()

########################################################################


def error_log(type, msg):
    with open("error_log.txt", "a", errors='ignore', encoding="utf8") as errorlog:
        print(f"{now} {type}: {msg}", file=errorlog)
    print("Error written into error_log.txt")


def create_folder(baselocation, folder_name):
    folder_name = folder_name.replace(':', '')
    folder_path = os.path.join(baselocation, folder_name)
    if os.path.exists(folder_path):
        pass
    else:
        try:
            os.makedirs(folder_path, exist_ok=True)
        except OSError:
            error_log("Folder error", "Creation of the directory " + str(folder_path) + " failed.")
            return False
        else:
            print("Successfully created the directory %s " % folder_path)
            return folder_path


def get_json_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        jsonResponse = response.json()
        return jsonResponse
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        error_log("HTTP", "HTTP error occurred: " + str(http_err))
    except Exception as err:
        print(f'Other error occurred: {err}')


def get_trailer_id(video_id, type):
    trailer_id = get_json_from_api('https://api.themoviedb.org/3/' + str(type) + '/' + str(video_id) + '/videos?api_key=' + str(API_KEY) + '&language=' + str(LANGUAGE))
    trailer_list = []
    trailer_results = trailer_id['results']
    if trailer_results:
        if type == "movie":
            return trailer_results[0]['key']
        else:
            for trail in trailer_results:
                trailer_list.append(trail['key'])
            return trailer_list
    else:
        print("No available video, trailer, or whatever.")
        error_log("TRAILER_ID", "Video " + str(video_id) + " does not have any videos.")
        return False


def get_movies(page):
    movie_id = get_json_from_api('https://api.themoviedb.org/3/movie/popular?api_key=' + str(API_KEY) + '&language=' + str(LANGUAGE) + '&page=' + str(page))
    movie_results = movie_id['results']
    for m in movie_results:
        tmdb_id = m['id']
        tmdb_title = m['title']
        tmdb_title = tmdb_title.replace(':', '')
        if "release_date" in m:
            tmdb_year = m['release_date'][:4]
            print("-"*30)
            print(f"{tmdb_title} ({tmdb_year})")
            print(f"TMDB Id: {tmdb_id}")
            if tmdb_year >= AGE_YEAR:
                movie_f_title = tmdb_title + " (" + tmdb_year + ")"
                trailer_id = get_trailer_id(tmdb_id, "movie")
                print(f"Trailer Id: {trailer_id}")
                create_folder(MOVIE_LOCATION, movie_f_title)
                movie_file_name = movie_f_title + ".mp4"
                movie_file_location = os.path.join(MOVIE_LOCATION, movie_f_title, movie_file_name)
                if trailer_id:
                    if not os.path.exists(movie_file_location):
                        ydl_opts = {
                            'format': '137+140/136+140',
                            'ignoreerrors': True,
                            'source_address': '0.0.0.0',
                            'outtmpl': movie_file_location
                        }
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([trailer_id])
        else:
            error_log("RELEASE_YEAR", str(tmdb_title) + " does not have release date.")


def get_tvshows(page):
    tvshow_id = get_json_from_api('https://api.themoviedb.org/3/tv/popular?api_key=' + str(API_KEY) + '&language=' + str(LANGUAGE) + '&page=' + str(page))
    tvshow_results = tvshow_id['results']
    for m in tvshow_results:
        tmdb_id = m['id']
        tmdb_title = m['name']
        tmdb_title = tmdb_title.replace(':', '')
        if "first_air_date" in m:
            tmdb_year = m['first_air_date'][:4]
            print("-" * 30)
            print(f"{tmdb_title} ({tmdb_year})")
            print(f"TMDB Id: {tmdb_id}")
            if tmdb_year >= AGE_YEAR:
                tvshow_f_folder = tmdb_title + " (" + tmdb_year + ")"

                trailer_id = get_trailer_id(tmdb_id, "tv")

                create_folder(TV_LOCATION, tvshow_f_folder)
                folder_location = os.path.join(TV_LOCATION, tvshow_f_folder)
                season_zero_location = os.path.join(TV_LOCATION, tvshow_f_folder, "Season 00")
                create_folder(folder_location, "Season 00")
                extra_content = 1
                if trailer_id:
                    for trail in trailer_id:
                        tvshow_f_title = "S00E0" + str(extra_content) + " - " + tvshow_f_folder
                        tvshow_file_name = tvshow_f_title + ".mp4"
                        tvshow_file_location = os.path.join(season_zero_location, tvshow_file_name)
                        if not os.path.exists(tvshow_file_location):
                            ydl_opts = {
                                'format': '137+140/136+140',
                                'ignoreerrors': True,
                                'source_address': '0.0.0.0',
                                'outtmpl': tvshow_file_location
                            }
                            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                ydl.download([trail])

                        extra_content += 1
        else:
            error_log("RELEASE_YEAR", str(tmdb_title) + " does not have release date.")


def main():
    mov_page = 1
    while mov_page <= int(PAGE_NO):
        get_movies(mov_page)
        mov_page += 1

    tv_page = 1
    while tv_page <= int(PAGE_NO):
        get_tvshows(tv_page)
        tv_page += 1


if __name__ == '__main__':
    main()
