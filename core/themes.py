from colorama import Fore

themes = {
    "default": {
        "banner": Fore.CYAN,
        "greeting": Fore.MAGENTA,
        "header": Fore.YELLOW,
        "result": Fore.GREEN,
        "command": Fore.YELLOW,
        "prompt": Fore.WHITE
    },
    "matrix": {
        "banner": Fore.GREEN,
        "greeting": Fore.LIGHTGREEN_EX,
        "header": Fore.WHITE,
        "result": Fore.LIGHTGREEN_EX,
        "command": Fore.WHITE,
        "prompt": Fore.GREEN
    },
    "neon": {
        "banner": Fore.MAGENTA,
        "greeting": Fore.CYAN,
        "header": Fore.YELLOW,
        "result": Fore.LIGHTMAGENTA_EX,
        "command": Fore.YELLOW,
        "prompt": Fore.CYAN
    },
    "ocean": {
        "banner": Fore.BLUE,
        "greeting": Fore.LIGHTCYAN_EX,
        "header": Fore.WHITE,
        "result": Fore.LIGHTBLUE_EX,
        "command": Fore.CYAN,
        "prompt": Fore.BLUE
    },
    "dark": {
        "banner": Fore.WHITE,
        "greeting": Fore.LIGHTBLACK_EX,
        "header": Fore.LIGHTWHITE_EX,
        "result": Fore.GREEN,
        "command": Fore.YELLOW,
        "prompt": Fore.WHITE
    }
}
