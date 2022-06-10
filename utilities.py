import requests
from bs4 import BeautifulSoup
from macros import *
from functools import wraps
import tracemalloc
from time import perf_counter

left_padding: str = '\t'
seinfeld_theme_music_file = 'media/seinfeld_theme_music.wav'
seinfeld_db_path = 'db'
#seinfeld_db_file = seinfeld_db_path + 'seinfeld_series_db'


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