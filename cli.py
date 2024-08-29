"""
"""
from __future__ import annotations

import fire
from salestrack.console import CliCommand as SalesTrackCommand


class Command:
    def __init__(self) -> None:
        self.salestrack = SalesTrackCommand


def main():
    fire.Fire(Command)
