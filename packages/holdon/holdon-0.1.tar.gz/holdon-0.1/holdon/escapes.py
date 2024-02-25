END = "\033[0m"

class ERASE:
    ENTIRE_LINE = "\033[2K"

class COLOR:
    PURPLE = "\033[0;35m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    CYAN = "\033[0;36m"
    
class CURSOR:
    HOME = "\033[H"
    RESTORE = "\033[u"
    SAVE = "\033[s"
    HIDE = "\033[?25l"
    SHOW = "\033[?25h"

    def next_line_begin(i: int = 1):
        return f"\033[{i}E"
    
    def prev_line_begin(i: int = 1):
        return f"\033[{i}F"

class STYLE:
    DARK = "\033[2m"
