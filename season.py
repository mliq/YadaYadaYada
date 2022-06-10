from episode import Episode
import concurrent.futures
from utilities import *
from pathlib import Path
import jsonpickle


class Season:

    def __init__(self, season: str):
        self.season: str = season
        self.episode_list: {str: Episode} = {}
        self.years: str = ""
        self.ep_count: int = 0

    def __str__(self):
        out_string = "#####################\n"
        out_string += f'    Season: {self.season}\n'
        out_string += f'    Episode Count: {self.ep_count}\n'
        out_string += "#####################\n\n"
        for episode in self.episode_list.values():
            out_string += episode.__str__()
        return out_string

    def add_episode(self, episode: Episode):
        self.episode_list[episode.episode_number] = episode
        self.ep_count += 1
        episode.save_episode_metadata()

    @measure_performance
    def load_scripts(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.ep_count) as executor:
            thread_pool = {}
            for episode in self.episode_list.values():
                if episode.script_loaded is not True:
                    print('new future - episode')
                    thread_pool[episode.episode_number] = executor.submit(episode.load_script)

            for future in concurrent.futures.as_completed(thread_pool.values()):
                print("\n Thread finished - episode == ", future.result())
        return f'{self.season}'

    def find_episode_by_epno(self, ep_no: int):
        pass

    def find_episode_by_name(self, ep_name: str):
        pass

    def get_episode_scripts(self):
        self.load_scripts()

    def print_scripts(self):
        for episode in self.episode_list.values():
            print('\n' + episode.__str__() + '\n')
            print(episode.script)
            print('\n       **********            \n\n')

    def find_dialogue_in_episode(self, dialogue: str, return_all_occurances: bool):
        for episode in self.episode_list.values():
            if episode.find_in_script(dialogue):
                print("Dialogue found in: ")
                print(episode)
                if return_all_occurances is True:
                    return True
        return False

