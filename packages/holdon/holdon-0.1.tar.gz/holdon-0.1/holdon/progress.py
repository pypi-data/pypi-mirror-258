import sys
import time
from typing import Iterator, Literal, Optional, Tuple, Union

from .escapes import COLOR, END, ERASE, STYLE

UnknownRatio = Tuple[Literal["?"], Literal["?"]]
ItRatio = Tuple[float, float]
StrRatio = Tuple[str, str]

def apply_to_bar(
    fmt: str, 
    percentage: int,
    width: int,
    speed: str,
    ratio: Union[ItRatio, StrRatio, UnknownRatio] = ("?", "?")
):
    # percentage
    pc_str = f"{percentage * 100:.1f}"
    perfect_pc = len("100.0")
    fmt = fmt.replace(
        "{percentage}", 
        " " * (perfect_pc - len(pc_str)) +
        COLOR.PURPLE + pc_str + "%" + END
    )

    # the progress bar
    filled_bars_count = int(width * percentage)
    if not filled_bars_count:
        fmt = fmt.replace(
            "{bar}",
            STYLE.DARK + "━" * width + END
        )
    elif percentage >= 1.0:
        fmt = fmt.replace(
            "{bar}",
            COLOR.GREEN + "━" * width + END
        )
    else:
        fmt = fmt.replace(
            "{bar}",
            COLOR.RED + "━" * filled_bars_count + 
            "\b" + "╸" + END + 
            STYLE.DARK + "━" * (width - filled_bars_count) + END
        )

    # fractions
    # (let nameof ratio = fractions)
    a, b = str(ratio[0]), str(ratio[1])
    perfect_rt = len(str(b))
    fmt = fmt.replace(
        "{fractions}",
        COLOR.CYAN + " " * (perfect_rt - len(a)) + f"{a} / {b}" + END
    )

    # average speed
    fmt = fmt.replace(
        "{avg}",
        STYLE.DARK + f"({speed}/s)" + END
    )

    return fmt

def get_size(obj: range) -> int:
    if isinstance(obj, range):
        # prevents from actually iterating
        return int((obj.stop - obj.start) / obj.step)

    elif type(obj) in (str, bytes, list, tuple, set, dict):
        return len(obj)
    
def human_readable_bytes(__bytes: int, suffix: str = "B"):
    # https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(__bytes) < 1024.0:
            return f"{__bytes:3.1f}{unit}{suffix}"
        __bytes /= 1024.0

    return f"{__bytes:.1f}Y{suffix}"

class RawProgress:
    fmt = "{percentage} {bar} {fractions} {avg}"

    def __init__(
        self, 
        width: int = 50, 
        size: int = 100,
        unit: Literal["it", "bytes"] = "it"
    ):
        self.width = width
        self.size = size
        self.i = 0
        self.unit = unit

        # for stats
        self.last_iter = time.time()
        self.last_total_i = 0
        self.avg_history = []

        # initial rendering
        self.render()


    def advance(self, i: int = 1):
        self.i += i
        self.last_total_i += i

        now = time.time()
        est = now - self.last_iter

        if est >= 0:
            try:
                avg = self.last_total_i / (time.time() - self.last_iter)
            except ZeroDivisionError:
                avg = self.i

            self.avg_history.append(avg)
            self.last_total_i = 0
            self.last_iter = now

        self.render()

    def render(self):
        avg = self.avg_history[-1] if self.avg_history else 0

        if self.unit == "it":
            speed = f"{avg:.1f}it"
        else:
            speed = f"{human_readable_bytes(avg)}"

        if self.i >= self.size:
            speed = "avg " + speed

        sys.stdout.write(
            ERASE.ENTIRE_LINE + 
            "\r" +
            apply_to_bar(
                self.fmt, 
                self.i / self.size, 
                self.width,
                ratio=(
                    (self.i, self.size)
                    if self.unit == "it" else
                    (human_readable_bytes(self.i), human_readable_bytes(self.size))
                ),
                speed=speed
            )
        )
        sys.stdout.flush()


def progress(
    iterator: Iterator, 
    *, 
    width: Optional[int] = None, 
    size: Optional[int] = None,
    unit: Literal["it", "bytes"] = "it"
) -> Iterator:
    """Creates a progress bar.

    .. code-block :: python

        for i in progress(range(100)):
            ... # do your work here


    Args:
        iterator (Iterator): The iterator. For instance, ``range`` or ``list``.
        width (int, optional): Width of the progress bar. Defaults to 50.
        size (int, optional): Size of the iterator or the ``len()`` of the iterator.
        unit (`Literal["it", "bytes"]`): Unit. Could be one of: "it" (iterations) or "bytes" (bytes).
    """
    rp = RawProgress(width or 50, size or get_size(iterator), unit=unit)

    try:
        for c in iterator:
            if unit == "bytes" and isinstance(c, bytes):
                advance = len(c)
            else:
                advance = 1

            rp.advance(advance)
            yield c

    finally:
        sys.stdout.write("\n")
        sys.stdout.flush()
