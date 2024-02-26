from . import mkdir
from . import ls
from . import cat
from . import tail
from . import less
from . import wc
from . import grep

COMMANDS = {
    "cat": cat.handle,
    "grep": grep.handle,
    "less": less.handle,
    "ls": ls.handle,
    "mkdir": mkdir.handle,
    "tail": tail.handle,
    "wc": wc.handle
}
