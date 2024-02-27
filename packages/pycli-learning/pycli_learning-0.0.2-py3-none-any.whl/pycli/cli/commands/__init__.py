from . import cat, grep, less, ls, mkdir, tail, wc

COMMANDS = {
    "cat": cat.handle,
    "grep": grep.handle,
    "less": less.handle,
    "ls": ls.handle,
    "mkdir": mkdir.handle,
    "tail": tail.handle,
    "wc": wc.handle,
}
