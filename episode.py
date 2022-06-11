from utilities import *
import jsonpickle
from pathlib import Path


class Episode:

    def __init__(self, season: str, name: str, ep_num: int, script_url: str):
        self.season: str = season
        self.name: str = name
        self.episode_number = ep_num
        self.date: str = ""
        self.script_url: str = script_url
        self.script: str = ""
        self.episode_urls = ""
        self.script_loaded: bool = False

    def __eq__(self, other):
        if self.name == other.name:
            if self.season == other.season:
                if self.episode_number == other.episode_number:
                    if self.script_url == other.script_url:
                        return True
        return False

    def get_printable_info(self):
        ep_info = f'{nl_leftpadding}Season: {self.season}'
        ep_info += f'{nl_leftpadding}Episode Number: {self.episode_number}'
        ep_info += f'{nl_leftpadding}Episode Name: {self.name}'
        return ep_info

    def __str__(self):
        return f'ep_no: {self.episode_number}, ep_name: {self.name}, script_url: {self.script_url}'

    def load_script(self):
        self.script = get_page_text_soup(self.script_url)
        self.script_loaded = True
        self.format_script()
        self.save_episode_script()
        return f'{self.episode_number}'

    def save_episode_metadata(self):
        ep_fs_path = f'{seinfeld_db_path}/{self.season}/{self.episode_number:03d}_{self.name}'
        episode_path = Path(ep_fs_path)
        if episode_path.exists() is not True:
            episode_path.mkdir(0o777, parents=True, exist_ok=True)

        episode_metadata_file = Path(f'{ep_fs_path}/metadata')
        with open(episode_metadata_file, 'a+') as file:
            file.write(jsonpickle.encode(self, indent=4))

    def format_script(self):
        top_marker: str = 'Looking for  a great gift idea for the holidays?'
        bottom_marker: str = 'Home\nFull Scripts\nCommunity'
        top_idx = self.script.find(top_marker)
        top_idx += self.script[top_idx:].find('\n')
        bottom_idx = self.script.rfind(bottom_marker)
        self.script = self.script[top_idx:bottom_idx]

    def save_episode_script(self):
        ep_fs_path = f'{seinfeld_db_path}/{self.season}/{self.episode_number:03d}_{self.name}'
        episode_path = Path(ep_fs_path)
        if episode_path.exists() is not True:
            episode_path.mkdir(mode=0o777, parents=True, exist_ok=True)

        episode_script_file = Path(f'{ep_fs_path}/script.txt')
        with open(episode_script_file, 'w') as file:
            file.write(self.script)

    def find_in_script(self, dialogue: str) -> bool:
        if self.script_loaded is not True:
            self.load_script()
        print(self)
        if self.script.lower().find(dialogue.lower()) != -1:
            return True
        return False


# episode = Episode(season='1',name='Seinfeld Chronicles',ep_num=1,script_url='https:\\www.seinfeldscripts.com')
# print(episode.__dict__)
# print(episode)
# print('-------------------------------------------')
# json_obj = jsonpickle.encode(episode, indent=4)
# rebuilt_obj = jsonpickle.decode(json_obj)
# print(json_obj)
# print('-------------------------------------------')
# print(rebuilt_obj.__dict__)
# print(rebuilt_obj)
# if episode == rebuilt_obj:
#     print('equal true')
# else:
#     print('equal false')
