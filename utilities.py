from pathlib import Path

import requests
from bs4 import BeautifulSoup
from macros import *
from functools import wraps
import tracemalloc
from time import perf_counter

left_padding: str = '\t'
nl_leftpadding: str = '\n\t'
seinfeld_theme_music_file = 'media/seinfeld_theme_music.wav'
george_living_society_file = 'media/george_living_in_a_society.wav'
frank_serenity_now_file = 'media/serenity_now.wav'
jerry_what_are_we_doing_file = 'media/jerry_what_in_gods_name.wav'
kramer_giddy_up_file = 'media/kramer_giddy_up.wav'
elaine_yadayadayada_file = 'media/elaine_yada_yada_yada.wav'
elain_getout_file = 'media/elain_get_out.wav'

seinfeld_db_path = 'db'
app_logfile_path = 'logs'
app_logfile_name = f'yada_yada_yada.log'
app_logfile = f'{app_logfile_path}/{app_logfile_name}'


def create_dir(dir_path: str):
    directory = Path(dir_path)
    if directory.exists() is not True:
        directory.mkdir(0o777, parents=True, exist_ok=True)


def get_html_page_soup(url: str) -> BeautifulSoup:
    page = requests.get(url, headers=headers, timeout=10)
    page_html = page.text
    return BeautifulSoup(page_html, 'html.parser')


def get_page_text_soup(url: str) -> str:
    return get_html_page_soup(url).text


def measure_performance(func):
    '''Measure performance of a function'''

    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = perf_counter()
        func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        finish_time = perf_counter()
        print(f'Function: {func.__name__}')
        print(f'Method: {func.__doc__}')
        print(f'Memory usage:\t\t {current / 10 ** 6:.6f} MB \n'
              f'Peak memory usage:\t {peak / 10 ** 6:.6f} MB ')
        print(f'Time elapsed is seconds: {finish_time - start_time:.6f}')
        print(f'{"-" * 40}')
        tracemalloc.stop()

    return wrapper
