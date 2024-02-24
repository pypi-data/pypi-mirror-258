import logging
import json
import os
import pydantic
# import pathlib

from rich.console import Console
# from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from . import constants
from .console_helper import print_yellow, print_red
from .util import search_todos, search_fixmes

console = Console()


DEFAULT_OUTDIR = os.path.join(
    constants.DEFAULT_OUTDIR_BASE,
    os.path.splitext(os.path.basename(__file__))[0],
    constants.DEFAULT_TIMESTAMP,
)

class Record(pydantic.BaseModel):
    filepath: str
    content: str
    line_number: int
    author: Optional[str]
    priority: Optional[str]
    issue_id: Optional[str]

class TodoRecord(Record):
    pass

class FixmeRecord(Record):
    pass

class Manager:

    def __init__(self, **kwargs):
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", constants.DEFAULT_CONFIG_FILE)
        self.indir = kwargs.get("indir", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", DEFAULT_OUTDIR)
        self.outfile = kwargs.get("outfile", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self.todo_records = []
        self.fixme_records = []

        logging.info(f"Instantiated Manager in '{os.path.abspath(__file__)}'")

    def scan_codebase(self) -> None:
        todos = search_todos(self.indir)
        fixmes = search_fixmes(self.indir)
        self._generate_report(self.outfile, todos, fixmes)


    def _generate_report(self, outfile: Optional[str], todos: List[Dict[str, str]], fixmes: List[Dict[str, str]]) -> None:
        if outfile is None or outfile == "":
            outfile = self.outfile

        lookup = {
            "method-created": os.path.abspath(__file__),
            "date-created": str(datetime.today().strftime('%Y-%m-%d-%H%M%S')),
            "created-by": os.environ.get('USER'),
            "logfile": self.logfile,
            "indir": self.indir,
            "todos": todos,
            "fixmes": fixmes,
        }

        # Write dictionary to output JSON file
        with open(outfile, 'w') as f:
            f.write(json.dumps(lookup, indent=4))

        if self.verbose:
            console.print(f"Wrote report to '{outfile}'")
        logging.info(f"Wrote report to '{outfile}'")

    def create_todo_md(self, outfile: Optional[str]) -> None:
        todos = search_todos(self.indir)
        fixmes = search_fixmes(self.indir)

        if outfile is None or outfile == "":
            outfile = self.outfile

        with open(outfile, 'w') as of:
            of.write(f"method-created: {os.path.abspath(__file__)}<br>\n")
            of.write(f"date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}<br>\n")
            of.write(f"created-by: {os.environ.get('USER')}<br>\n")
            of.write(f"indir: {self.indir}<br>\n")
            of.write(f"logfile: {self.logfile}<br>\n")

            if len(todos) > 0:
                of.write("# TODOs\n")
                for i, todo in enumerate(todos):
                    of.write(f"{i+1}. {todo['comment']}<br>\n")
                    of.write(f"{todo['file']}:{todo['line']}<br>\n<br>\n")
            else:
                console.print("No TODOs found")
                logging.warning("No TODOs found")

            if len(fixmes) > 0:
                of.write("\n# FIXMEs\n")
                for i, fixme in enumerate(fixmes):
                    of.write(f"{i+1}. {fixme['comment']}<br>\n")
                    of.write(f"{fixme['file']}:{fixme['line']}<br>\n<br>\n")
            else:
                console.print("No FIXMEs found")
                console.warning("No FIXMEs found")

        logging.info(f"Wrote file '{outfile}'")
        if self.verbose:
            console.print(f"Wrote TODO file '{outfile}'")

