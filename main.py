from series_info import *
import concurrent.futures
from ui_manager import *


# MAIN
# if __name__ == '__main__':
#     fetch_series_info()
#     start = timer()
#     print('before')
#     executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
#     load_bg_thread = [executor.submit(load_scripts)]
#     print('after')
#
#     print('I have started loading in backgroud')
#     for thread in concurrent.futures.as_completed(load_bg_thread):
#         print('\n\n\nLOAD Thread finished')
#         end = timer()
#         print('\n--------- from main thread - load time: ', (end - start))
#         print(series_loaded)
#
#     print_seasons()
#     print_season_scripts()
#
#
#     exit(1)


if __name__ == '__main__':
    seinfeld = SeinfeldSeries()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    load_bg_thread = [executor.submit(seinfeld.prefetch_seinfeld_db)]

    header = Header('Yada Yada Yada', 'v0.1')
    ui = UiManager(header)
    ui.startup()
    ui.main_loop()
    ui.shutdown()
