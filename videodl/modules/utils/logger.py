'''
Function:
    Implementation of Logging Related Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import shutil
import logging
import collections.abc
from prettytable import PrettyTable
from platformdirs import user_log_dir


'''settings'''
COLORS = {'red': '\033[31m', 'green': '\033[32m', 'yellow': '\033[33m', 'blue': '\033[34m', 'pink': '\033[35m', 'cyan': '\033[36m', 'highlight': '\033[93m', 'number': '\033[96m'}


'''LoggerHandle'''
class LoggerHandle():
    appname, appauthor = 'videodl', 'zcjin'
    os.makedirs((log_dir := user_log_dir(appname=appname, appauthor=appauthor)), exist_ok=True)
    log_file_path = os.path.join(log_dir, "videodl.log")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler(log_file_path, encoding="utf-8"), logging.StreamHandler()])
    '''log'''
    @staticmethod
    def log(level, message): logging.getLogger(LoggerHandle.appname).log(level, str(message))
    '''debug'''
    @staticmethod
    def debug(message: str, disable_print: bool = False): message = str(message); open(LoggerHandle.log_file_path, 'a', encoding='utf-8').write(message + '\n') if disable_print else LoggerHandle.log(logging.DEBUG, message)
    '''info'''
    @staticmethod
    def info(message: str, disable_print: bool = False): message = str(message); open(LoggerHandle.log_file_path, 'a', encoding='utf-8').write(message + '\n') if disable_print else LoggerHandle.log(logging.INFO, message)
    '''warning'''
    @staticmethod
    def warning(message: str, disable_print: bool = False): message = str(message); open(LoggerHandle.log_file_path, 'a', encoding='utf-8').write(message + '\n') if disable_print else LoggerHandle.log(logging.WARNING, message if '\033[31m' in message else colorize(message, 'red'))
    '''error'''
    @staticmethod
    def error(message: str, disable_print: bool = False): message = str(message); open(LoggerHandle.log_file_path, 'a', encoding='utf-8').write(message + '\n') if disable_print else LoggerHandle.log(logging.ERROR, message if '\033[31m' in message else colorize(message, 'red'))


'''printtable'''
def printtable(titles, items, terminal_right_space_len=4):
    assert isinstance(titles, collections.abc.Sequence) and isinstance(items, collections.abc.Sequence), 'title and items should be iterable'
    table = PrettyTable(titles); tuple(table.add_row(item) for item in items)
    max_width = shutil.get_terminal_size().columns - terminal_right_space_len
    assert max_width > 0, f'"terminal_right_space_len" should smaller than {shutil.get_terminal_size()}'
    table.max_table_width = max_width; print(table)
    return table


'''colorize'''
def colorize(string, color):
    string = str(string)
    if color not in COLORS: return string
    return COLORS[color] + string + '\033[0m'


'''printfullline'''
def printfullline(ch: str = "*", end: str = '\n', terminal_right_space_len: int = 1):
    cols = shutil.get_terminal_size().columns - terminal_right_space_len
    assert cols > 0, f'"terminal_right_space_len" should smaller than {shutil.get_terminal_size()}'
    print(ch * cols, end=end)