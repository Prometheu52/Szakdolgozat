from enum import Enum
from colorama import Style, Fore

class Log(Enum):
    INFO = 1
    WARN = 2
    ERROR = 3

def log(level: Log, message):
    match level:
        case level.INFO:
            print(Fore.WHITE + "[" + Fore.LIGHTCYAN_EX + "INFO" + Fore.WHITE + "]" + Style.RESET_ALL, message)
        case level.WARN:
            print(Fore.WHITE + "[" + Fore.LIGHTYELLOW_EX + "WARN" + Fore.WHITE + "]" + Style.RESET_ALL, message)
        case level.ERROR:
            print(Fore.WHITE + "[" + Fore.LIGHTRED_EX + "ERROR" + Fore.WHITE + "]" + Style.RESET_ALL, message)
