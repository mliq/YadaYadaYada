import os
import time
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # to stop pygame module from printing version at import
import pygame.mixer
from utilities import *
from enum import Enum
from sty import fg, bg, ef, rs
from seinfeld_series import *

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


class AudioMgr:

    def __init__(self):
        pygame.mixer.init()
        self.bg_audio_obj: pygame.mixer.Sound = pygame.mixer.Sound(file=seinfeld_theme_music_file)

    def play_seinfeld_theme_bg(self, play: bool = True):
        if play is True:
            self.bg_audio_obj.set_volume(0.03)
            self.bg_audio_obj.play(loops=-1)
        else:
            self.bg_audio_obj.stop()

    def play_living_in_society(self):
        sound_obj: pygame.mixer.Sound = pygame.mixer.Sound(file=george_living_society_file)
        sound_obj.set_volume(0.2)
        sound_obj.play()

    def play_serenity_now(self):
        sound_obj: pygame.mixer.Sound = pygame.mixer.Sound(file=frank_serenity_now_file)
        sound_obj.set_volume(0.1)
        sound_obj.play()

    def play_what_are_we_doing(self):
        sound_obj: pygame.mixer.Sound = pygame.mixer.Sound(file=jerry_what_are_we_doing_file)
        sound_obj.set_volume(0.5)
        sound_obj.play()

    def play_giddy_up(self):
        sound_obj: pygame.mixer.Sound = pygame.mixer.Sound(file=kramer_giddy_up_file)
        sound_obj.set_volume(0.1)
        sound_obj.play()

    def play_yadayadayada_exit(self):
        sound_obj: pygame.mixer.Sound = pygame.mixer.Sound(file=elaine_yadayadayada_file)
        sound_obj.set_volume(0.1)
        sound_obj.play()

    def play_getout(self):
        sound_obj: pygame.mixer.Sound = pygame.mixer.Sound(file=elain_getout_file)
        sound_obj.set_volume(0.1)
        sound_obj.play()


class UiManager:

    def __init__(self, header: Header, audio_mgr: AudioMgr, seinfeld: SeinfeldSeries):
        self.header = header
        self.seinfeld = seinfeld
        self.audio_mgr = audio_mgr

    def display_menu(self, menu: dict):
        self.display_header()
        for menu_id, menu_item in menu.items():
            #print(str(menu_id) + '----' + menu_item)
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

        print(f'{msg}', end=end * 2)
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

    def startup(self):
        self.startup_screen()

    def startup_screen(self):
        self.display_header()
        self.progress_bar('prefetching yada yada yada in the background...',
                          loading_chars='|', bar_size=65, speed=ProgressBarSpeed.slow)

    def shutdown(self):
        self.audio_mgr.play_yadayadayada_exit()
        self.shutdown_screen()
        exit(0)

    def shutdown_screen(self):
        self.display_header()
        self.progress_bar('Don\'t go!!!\n\tI\'m disturbed, I\'m depressed, I\'m inadequate. I\'ve got it all!',
                          loading_chars='.', bar_size=65, speed=ProgressBarSpeed.very_slow)
        pass

    def get_user_menu_choice(self, menu_list: dict) -> int:
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
                    self.audio_mgr.play_living_in_society()
                    self.print_animated_dialogue('You know', 'WE ARE LIVING IN A SOCIETY!!!',
                                                 speed=ProgressBarSpeed.fast)
                    input('\t')
                else:
                    print()
                    display_menu = True
                    failed_input_counter = 0
                    time.sleep(0.5)
                    self.display_header()
                    self.audio_mgr.play_serenity_now()
                    self.print_animated_dialogue('SERENITY NOW', '', loading_chars='!', speed=ProgressBarSpeed.slow)
                    input('\t')
                pass
        return choice

    def search_dialogue(self):
        input_dialogue: str = ''
        valid_choice: bool = False
        failed_input_counter: int = 0
        display_header: bool = False
        self.display_header()

        while not valid_choice:
            try:
                if display_header is True:
                    self.display_header()
                    display_header = False

                input_dialogue = str(input(f'\tWhat is the dialogue you want to search for?\n\t'))
                valid_choice = True
            except ValueError:
                print(f'\n\tGeorge\'s getting upset!!! You have not entered a valid string!')
                failed_input_counter += 1
                if failed_input_counter < 3:
                    print()
                    self.print_animated_dialogue('You know', 'WE ARE LIVING IN A SOCIETY!!!',
                                                 speed=ProgressBarSpeed.fast)
                    input('\t')
                else:
                    print()
                    failed_input_counter = 0
                    display_header = True
                    time.sleep(0.5)
                    self.display_header()
                    self.print_animated_dialogue('SERENITY NOW', '', loading_chars='!', speed=ProgressBarSpeed.slow)
                    input('\t')
                pass
        ep = self.seinfeld.search_dialogue(input_dialogue)
        if ep is None:
            self.audio_mgr.play_what_are_we_doing()
            print(f'\n\n\tOops! No such dialogue in Seinfeld series.')
            self.print_animated_dialogue('\n\tWhat in God\'s name are you doing ', '', loading_chars='?', speed=ProgressBarSpeed.very_slow)
        else:
            self.display_header()
            print('\n\n\tFound the episode....\n')
            print(ep.get_printable_info())
            # TODO: option to read full episode script by taking input
            print('\n\n')

            try:
                user_choice = str(input('\tDo you want to read the full script of this episode? (Y/N) : '))
                if user_choice.lower() == 'y':
                    self.display_header()
                    self.audio_mgr.play_giddy_up()
                    self.progress_bar('loading the script...',
                                      loading_chars='>', bar_size=65, speed=ProgressBarSpeed.slow)
                    print(ep.script)
                    input()
                    self.print_animated_dialogue('Going back to main menu', '', loading_chars='.',
                                                 speed=ProgressBarSpeed.slow)
                else:
                    self.audio_mgr.play_getout()
                    self.print_animated_dialogue('Going back to main menu', '', loading_chars='.',
                                                 speed=ProgressBarSpeed.slow)
            except ValueError:
                pass


    def read_script(self):
        print('read_script....')
        time.sleep(3)

    def get_random_dialogue(self):
        print('get_random_dialogue....')
        time.sleep(3)

    def exit_main_menu(self):
        print('exit_main_menu....')
        self.shutdown()

    def main_menu(self):
        menu_list = {1: 'Find which episode a dialogue is from',
                     2: 'Browse complete episode scripts',
                     3: 'Show random dialogues from the series',
                     4: 'Exit'}
        stop_flag: bool = False
        while stop_flag is False:
            user_option = self.get_user_menu_choice(menu_list)
            if user_option == 1:
                self.search_dialogue()
            elif user_option == 2:
                pass
            elif user_option == 3:
                pass
            elif user_option == 4:
                self.shutdown()
            pass


    def run(self):
        # main_menu_list = {
        #     1: ['Search for a dialogue', self.search_dialogue],
        #     2: ['Search for a dialogue', self.read_script],
        #     3: ['Show random dialogues from the series', self.get_random_dialogue],
        #     4: ['Exit', self.exit_main_menu]
        # }
        # main_menu = Menu(main_menu_list,ui=self,is_main_menu=True)
        # main_menu.menu_loop()
        self.startup()
        self.main_menu()
        self.shutdown()

# TODO: Write a generic Menu class that takes care of
#       1. printing menu 2. taking input 3. executing option handler function
# class Menu:
#
#     def __init__(self, menu_list_funcs, ui: UiManager, is_main_menu: bool = False):
#         self.menu_list = menu_list_funcs
#         self.ui_mgr = ui
#         self.is_main_menu = is_main_menu
#         self.user_input_hint: str = 'Select option from menu: '
#         self.invalid_input_err_hint: str = 'Invalid! Enter a valid option!'
#
#     def get_menu_option_func(self, choice: int):
#         return self.menu_list[choice][1]
#
#     def get_user_input_int(self):
#         choice: int = 0
#         valid_choice: bool = False
#         while not valid_choice:
#             try:
#                 choice = int(input(f'\t{self.user_input_hint}'))
#             except ValueError:
#                 print(f'\n\t{self.invalid_input_err_hint}')
#
#         return choice
#
#
#     def menu_loop(self):
#         # main_menu = [{1: 'Search for a dialogue', 'func': search_dialogue},
#         #              {2: 'Browse episode scripts', 'func': read_script},
#         #              {3: 'Show random dialogues from the series', 'func': get_random_dialogue},
#         #              {4: 'Exit', 'func': exit_main_menu}]
#         # menu = {
#         #     1: ['Search for a dialogue', search_dialogue],
#         #     2: ['Search for a dialogue', read_script],
#         #     3: ['Show random dialogues from the series', get_random_dialogue],
#         #     4: ['Exit', exit_main_menu]
#         # }
#         stop_flag: bool = False
#         while stop_flag is False:
#             user_option = self.get_user_input_int()
#             option_handler = self.get_menu_option_func(user_option)
#             option_handler()
#             # run infinitely only in main menu, in all other menus, exit the chain to go back to main menu loop
#             if self.is_main_menu is not True:
#                 stop_flag = True
