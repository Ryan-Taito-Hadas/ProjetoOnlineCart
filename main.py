import io
import sys

from src.ui.terminal_app import main


def _configure_utf8_io() -> None:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8")


if __name__ == "__main__":
    _configure_utf8_io()
    main()