from time import sleep
from episode import Episode
from season import Season
from utilities import *
from pathlib import Path
from pathlib import PureWindowsPath
import jsonpickle


class SeinfeldSeries:
    def __init__(self):
        self.seinfeld_series_db: {str: Season} = {}
        self.series_loaded: bool = False
        pass

    def print_seasons(self, season: str = None):
        if season is not None:
            print(self.seinfeld_series_db[season].__str__())
        else:
            for season in self.seinfeld_series_db.values():
                print(season.__str__())

    def load_scripts(self):
        for season in self.seinfeld_series_db.values():
            season.load_scripts()
            sleep(1)
        self.series_loaded = True

    def print_season_scripts(self, season: str = None):
        if season is not None:
            self.seinfeld_series_db[season].print_scripts()
        else:
            for season in self.seinfeld_series_db.values():
                season.print_scripts()

    def find_dialogue(self, dialogue: str, return_all_occurences: bool = False):
        for season in self.seinfeld_series_db.values():
            if season.find_dialogue_in_episode(dialogue, return_all_occurences) is True:
                break

    def fetch_series_info(self):
        parser = get_html_page_soup(scripts_main_url)
        table_rows = parser.find_all("table", attrs={'border': '1'})
        counter: int = 0
        season: int = 1
        episode_num: int = 0

        for table in table_rows:  # each table obj contains rows with Title + Episodes sequence
            if str(season) not in self.seinfeld_series_db.keys():
                season_obj = Season(str(season))
                self.seinfeld_series_db[str(season)] = season_obj

            for row in table.find_all('tr'):  # each row either has Season OR HREF attribute with episode script link
                if row.text.find('Season') != -1 and row.text.find('Season 1') == -1:
                    season += 1
                    if str(season) not in self.seinfeld_series_db.keys():
                        season_obj = Season(str(season))
                        self.seinfeld_series_db[str(season)] = season_obj
                else:
                    for ahref in row.find_all('a'):
                        ep_name = ahref.text.strip().replace('\n', '')
                        episode_num += 1
                        ep_script_url = ahref['href'].strip()
                        episode_obj = Episode(str(season), ep_name, episode_num,
                                              seinfeld_scripts_home_url + ep_script_url)
                        self.seinfeld_series_db[str(season)].add_episode(episode_obj)

    def load_from_disk(self):
        db_dir = Path(seinfeld_db_path)
        for season_dir in db_dir.iterdir():
            season = PureWindowsPath(season_dir).name
            if season not in self.seinfeld_series_db.keys():
                self.seinfeld_series_db[season] = Season(season)

            for episode_dir in season_dir.iterdir():
                metadata_file = episode_dir.__str__() + '\\' + 'metadata'
                episode = None
                with open(metadata_file, 'r+') as file:
                    metadata = file.read()
                    episode = jsonpickle.decode(metadata)
                    self.seinfeld_series_db[season].add_episode(episode)

                script_file = episode_dir.__str__() + '\\' + 'script.txt'
                with open(script_file, 'r+') as file:
                    episode.script = file.read()
                #
                # print('*******************')
                # for episode in self.seinfeld_series_db[season].episode_list.values():
                #     print(episode.script)
        self.series_loaded = True

    def prefetch_seinfeld_db(self):
        self.load_from_disk()
        if self.series_loaded is False:
            self.fetch_series_info()
            self.load_scripts()

#
# #print(glob.glob('db/*/*',recursive=True))
# seinfeld_series_db: {str: Season} = {}
# db_dir = Path(seinfeld_db_path)
# for season_dir in db_dir.iterdir():
#     season = PureWindowsPath(season_dir).name
#     print('season --- ', season)
#     if season not in seinfeld_series_db.keys():
#         seinfeld_series_db[season] = Season(season)
#
#     for episode_dir in season_dir.iterdir():
#         metadata_file = episode_dir.__str__() + '\\' + 'metadata'
#         print(metadata_file)
#         with open(metadata_file, 'r+') as file:
#             metadata = file.read()
#             episode = jsonpickle.decode(metadata)
#             seinfeld_series_db[season].add_episode(episode)
#
#         script_file = episode_dir.__str__() + '\\' + 'script.txt'
#         with open(script_file, 'r+') as file:
#             episode.script = file.read()
#
#         print('*******************')
#         for episode in seinfeld_series_db[season].episode_list.values():
#             print(episode.script)
