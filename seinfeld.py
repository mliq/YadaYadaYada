import concurrent.futures
from ui_manager import *
import logging

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

app_name = 'Yada Yada Yada'
app_version = 'v0.1'


def configure_logging():
    create_dir(app_logfile_path)
    log_format = f'%(asctime)s %(processName)s[%(process)d] thread[%(threadName)s:%(thread)d] %(levelname)s ' \
                 f'%(module)s[line:%(lineno)d] %(funcName)s: %(message)s'
    logging.basicConfig(filename=app_logfile, format=log_format, encoding='utf-8', level=logging.DEBUG)


if __name__ == '__main__':
    configure_logging()
    logger = logging.getLogger('root')
    header = Header('Yada Yada Yada', 'v0.1')
    logger.debug(f'Started: {app_name} {app_version}')
    audio_mgr = AudioMgr()
    audio_mgr.play_seinfeld_theme_bg(play=True)
    seinfeld = SeinfeldSeries()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    # prefetch all episode data and save in filesystem
    load_bg_thread = [executor.submit(seinfeld.prefetch_seinfeld_db)]

    ui = UiManager(header, audio_mgr, seinfeld)
    seinfeld.set_ui_manager(ui)
    ui.run()

