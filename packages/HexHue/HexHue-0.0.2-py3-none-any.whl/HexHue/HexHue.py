class Text:
    GRAY = '\033[30m'
    GREY = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    LIGHT_GRAY = '\033[90m'
    LIGHT_GREY = '\033[90m'
    LIGHT_RED = '\033[31m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'
    LIGHT_WHITE = '\033[97m'

    RESET = '\033[39m'

class Back:
    GRAY = '\033[100m'
    GREY = '\033[100m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    WHITE = '\033[47m'

    LIGHT_RED = '\033[101m'
    LIGHT_GREEN = '\033[102m'
    LIGHT_YELLOW = '\033[103m'
    LIGHT_MAGENTA = '\033[105m'
    LIGHT_CYAN = '\033[106m'
    LIGHT_BLUE = '\033[104m'
    LIGHT_WHITE = '\033[107m'

    RESET = '\033[49m'

class Type:
    BOLD = '\033[1m'
    SEMI_BOLD = '\033[2m'
    NORMAL = '\033[22m'

class Hex:
    RESET_ALL = '\033[0m'
    NEW_LINE = '\n'
    @staticmethod
    def convert_to_ansi(hex_color_code):
        if hex_color_code[0] == '#':
            hex_color_code = hex_color_code[1:]
        r, g, b = int(hex_color_code[0:2], 16), int(hex_color_code[2:4], 16), int(hex_color_code[4:6], 16)
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def hex(hex_color_code):
        return Hex.convert_to_ansi(hex_color_code)

    def __getattr__(self, name):
        if len(name) == 6 or (len(name) == 7 and name.startswith("#")):
            hex_code = name.lstrip('#')
            return self.convert_to_ansi(hex_code)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

Hex = Hex()