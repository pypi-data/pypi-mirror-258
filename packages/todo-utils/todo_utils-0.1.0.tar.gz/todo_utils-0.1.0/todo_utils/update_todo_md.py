"""Scan the codebase at the specified directory and compile all TODO and FIXME comments and write a TODO.md."""
import click
import logging
import os
import pathlib
import sys
import yaml

from datetime import datetime
from rich.console import Console

from enum import Enum
from pathlib import Path
from typing import Dict, List, Union, Optional, Tuple

from . import constants
from .console_helper import print_yellow, print_green
from .manager import Manager
from .file_utils import check_infile_status, check_indir_status

DEFAULT_OUTDIR = os.path.join(
    constants.DEFAULT_OUTDIR_BASE,
    os.path.splitext(os.path.basename(__file__))[0],
    constants.DEFAULT_TIMESTAMP,
)

DEFAULT_INDIR = os.path.realpath(os.getcwd())

error_console = Console(stderr=True, style="bold red")

console = Console()


def validate_verbose(ctx, param, value):
    """Validate the validate option.

    Args:
        ctx (Context): The click context.
        param (str): The parameter.
        value (bool): The value.

    Returns:
        bool: The value.
    """

    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return constants.DEFAULT_VERBOSE
    return value


@click.command()
@click.option('--config_file', type=click.Path(exists=True), help=f"Optional: The configuration file for this project - default is '{constants.DEFAULT_CONFIG_FILE}'")
@click.option('--indir', help=f"Optional: The directory that should be scanned - default is '{DEFAULT_INDIR}'")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help=f"Optional: The output directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help=f"Optional: The output file - default is '{DEFAULT_OUTDIR}/scan_codebase.txt'")
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{constants.DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(
    config_file: str,
    indir: str,
    logfile: str,
    outdir: str,
    outfile: str,
    verbose: bool
):
    """Scan the codebase at the specified directory and compile all TODO and FIXME comments."""
    error_ctr = 0

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    if config_file is None:
        config_file = constants.DEFAULT_CONFIG_FILE
        print_yellow(f"--config_file was not specified and therefore was set to '{config_file}'")

    if indir is None:
        indir = DEFAULT_INDIR
        print_yellow(f"--indir was not specified and therefore was set to '{indir}'")

    check_indir_status(indir)

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        print_yellow(f"--outdir was not specified and therefore was set to '{outdir}'")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        print_yellow(f"Created output directory '{outdir}'")

    if logfile is None:
        logfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.log'
        )
        print_yellow(f"--logfile was not specified and therefore was set to '{logfile}'")

    if outfile is None:
        outfile = os.path.join(
            outdir,
            "TODO.md"
        )
        print_yellow(f"--outfile was not specified and therefore was set to '{outfile}'")

    logging.basicConfig(
        filename=logfile,
        format=constants.DEFAULT_LOGGING_FORMAT,
        level=constants.DEFAULT_LOGGING_LEVEL,
    )

    check_infile_status(config_file, "yaml")

    logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(Path(config_file).read_text())

    manager = Manager(
        config=config,
        config_file=config_file,
        indir=indir,
        outdir=outdir,
        outfile=outfile,
        logfile=logfile,
        verbose=verbose,
    )

    manager.create_todo_md(outfile)

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()

