#!/usr/bin/env python
import os
import re
import subprocess

import click


@click.command(
    context_settings=dict(
        ignore_unknown_options=True, allow_extra_args=True, help_option_names=["--noop"]
    ),
)
@click.argument("celery_args", nargs=-1, type=click.UNPROCESSED)
def command(celery_args):
    try:
        text = subprocess.check_output(grep_cmd(), shell=True, text=True)
    except subprocess.CalledProcessError as ex:
        if ex.returncode == 1:
            click.secho(
                "Error: Failed to automatically detect a celery app using :"
                f"cmd=`{grep_cmd()}`",
                fg="red",
            )
            raise click.Abort()

    lines = text.strip().split("\n", maxsplit=1)
    if len(lines) > 1:
        click.secho(
            ("Found multiple Celery apps. Unable to autodetect app. " f"Apps: {lines}"),
            fg="red",
        )
    celery_config_line = lines[0]
    celery_config_module = (
        celery_config_line.split(":")[0].replace("/", ".").replace(".py", "")
    )
    celery_app_var = re.search(r":(\w+)\s", celery_config_line).group(1)
    os.execlp("celery", f"--app={celery_config_module}:{celery_app_var}", *celery_args)


def grep_cmd():
    return "grep -r --exclude-dir='.*' --include='*.py' '= Celery('"


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    command()
