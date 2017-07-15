import os
import sys
import importlib

import click


@click.group()
@click.version_option("0.1-alpha")
def cli():
    pass


@cli.command()
@click.option("--application", "-a", help="Application instance to use")
def worker(application):
    _add_current_working_directory_to_path()
    try:
        module = importlib.import_module(application)
    except (ImportError, AttributeError) as exc:
        raise click.BadParameter(str(exc), param_hint='--application')

    module.wqueue.start()


def _add_current_working_directory_to_path():
    sys.path.append(os.getcwd())


if __name__ == '__main__':
    cli()
