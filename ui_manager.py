import os
import time
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'   #to stop pygame module from printing version at import
import pygame.mixer as audio_mgr
from utilities import *
from enum import Enum
from sty import fg, bg, ef, rs


class ProgressBarSpeed(Enum):
    very_slow = 4
    slow = 2
    fast = 0.9
    very_fast = 0.2


# Class of different styles
class Style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class Header:

    def __init__(self, app_name: str, app_ver: str):
        self.app_name: str = app_name
        self.app_ver: str = app_ver
        self.header_string: str = self.to_string()
        os.system('color')

    def to_string(self):
        header_string: str = ''
        header_string += f'#######################################################################\n'
        header_string += f'{left_padding * 3}' \
                         f'{bg.yellow}{fg.white} {self.app_name} {fg.rs}{bg.rs}' \
                         f'{bg.blue}{fg.white} {self.app_ver}{fg.rs}{bg.rs}\n'
        header_string += f'-----------------------------------------------------------------------\n'
        header_string += f'{Style.BLUE}{left_padding * 1} Read Seinfeld scripts\n' \
                         f'{Style.YELLOW}{left_padding * 2} Find which season/episode a dialogue is from\n' \
                         f'{Style.RED}{left_padding * 3} Yada yada yada... there is more\n{Style.WHITE}'
        # header_string += f'{left_padding * 1}   {datetime.now().strftime("%A %d %b, %Y %H:%M:%S")}\n'
        header_string += f'#######################################################################\n'
        return header_string

    def __str__(self):
        return self.header_string


class UiManager:

    def __init__(self, header: Header):
        self.header = header
        audio_mgr.init()
        self.bg_audio_obj: audio_mgr.Sound = audio_mgr.Sound(file=seinfeld_theme_music_file)

    def display_menu(self, menu: dict):
        self.display_header()
        for menu_id, menu_item in menu.items():
            print(f'{left_padding * 2}{menu_id}. {menu_item}')
        print()

    def display_header(self, clear_screen: bool = True):
        if clear_screen is True:
            os.system('cls')
        print(self.header.__str__())

    def print_animated_dialogue(self, first_part: str, second_part: str,
                                loading_chars: str = '.', speed: ProgressBarSpeed = ProgressBarSpeed.fast):
        print(f'\t{first_part}', end='')
        self.progress_bar(loading_chars=loading_chars, inline=True, speed=speed)
        print(f'{second_part}')

    @staticmethod
    def progress_bar(msg: str = '', loading_chars: str = '|',
                     inline: bool = False, speed: ProgressBarSpeed = ProgressBarSpeed.fast, bar_size: int = 10):
        end = ''
        if inline is False:
            end = '\n'
            print()
        loading_char_len = len(loading_chars)
        if len(msg) == 0:
            msg = ''
        else:
            msg = f'{left_padding}{msg}'

        print(f'{msg}', end=end*2)
        duration = speed.value
        sleep_secs = duration / bar_size
        printed_char_count = 0
        for i in range(1, bar_size):
            print(loading_chars, end='', flush=True)
            printed_char_count += loading_char_len
            if printed_char_count < bar_size:
                time.sleep(sleep_secs)
            else:
                break

        if inline is False:
            print()

    def seinfeld_music_bg(self, play: bool = True):
        if play is True:
            self.bg_audio_obj.set_volume(0.03)
            self.bg_audio_obj.play(loops=-1)
        else:
            self.bg_audio_obj.stop()

    def startup(self):
        self.seinfeld_music_bg()
        self.startup_screen()

    def startup_screen(self):
        self.display_header()
        self.progress_bar('prefetching yada yada yada in the background...',
                          loading_chars='|', bar_size=65, speed=ProgressBarSpeed.slow)

    def shutdown(self):
        self.shutdown_screen()
        self.progress_bar('Don\'t go! I have got it all!!!!!')
        self.seinfeld_music_bg(False)
        pass

    def shutdown_screen(self):
        self.display_header()
        pass

    def get_user_choice(self, menu_list: dict) -> int:
        allowed_values = list(menu_list.keys())
        choice: int = 0
        valid_choice: bool = False
        failed_input_counter: int = 0
        choice_limit_str = f'({allowed_values[0]}-{allowed_values[-1]})'
        display_menu: bool = True
        while not valid_choice:
            try:
                if display_menu is True:
                    self.display_menu(menu_list)
                    display_menu = False

                choice = int(input(f'\tSelect {choice_limit_str}: '))
                if choice in allowed_values:
                    valid_choice = True
                else:
                    raise ValueError
            except ValueError:
                print(f'\n\tInvalid selection!!!')
                failed_input_counter += 1
                if failed_input_counter < 3:
                    print()
                    self.print_animated_dialogue('You know', 'WE ARE LIVING IN A SOCIETY!!!',
                                                 speed=ProgressBarSpeed.fast)
                    input('\t')
                else:
                    print()
                    display_menu = True
                    failed_input_counter = 0
                    time.sleep(0.5)
                    self.display_header()
                    self.print_animated_dialogue('SERENITY NOW', '', loading_chars='!', speed=ProgressBarSpeed.slow)
                    input('\t')
                pass
        return choice

    def main_menu(self):
        menu_list = {1: 'Search for a dialogue',
                     2: 'Browse episode scripts',
                     3: 'Show random dialogues from the series',
                     4: 'Exit'}
        stop_flag: bool = False
        while stop_flag is False:
            user_option = self.get_user_choice(menu_list)
            if user_option == 1:
                print()
            elif user_option == 2:
                pass
            elif user_option == 3:
                pass
            else:
                stop_flag = True
            pass

    def main_loop(self):
        self.main_menu()
